from __future__ import annotations

import argparse
import importlib
import importlib.util
import inspect
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from execute.replay_feed import ReplayFeed
    from execute.force_signal_smoke import build_forced_signal
except ModuleNotFoundError:
    from replay_feed import ReplayFeed
    from force_signal_smoke import build_forced_signal


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gb_brain.runtime")


@dataclass
class RuntimePolicy:
    bot_name: str
    profile: str
    broker: str
    market: str
    venue: str
    execution_mode: str


LEGACY_BROKERS = {"auto", "yfinance", "blofin-ws", "oanda-practice", "manual"}
PHASE2D_BROKERS = {"replay", "sim-forced"}


def _profile_to_bot_name(profile: str) -> str:
    p = (profile or "").strip().lower()
    if p == "gb-crypto-bot":
        return "GB-CRYPTO-BOT"
    if p == "gb-indices":
        return "GB-INDICES"
    if p in {"manual-signals", "manual_signals"}:
        return "MANUAL-SIGNALS"
    return (profile or "GB-BRAIN").replace("_", "-").upper()


def _resolve_auto_broker(profile: str) -> str:
    p = (profile or "").strip().lower()
    if p == "gb-crypto-bot":
        return "blofin-ws"
    if p == "gb-indices":
        return "oanda-practice"
    if p in {"manual-signals", "manual_signals"}:
        return "manual"
    return "yfinance"


def resolve_policy(args: argparse.Namespace) -> RuntimePolicy:
    broker = args.broker
    if broker == "auto":
        broker = _resolve_auto_broker(args.profile)

    bot_name = _profile_to_bot_name(args.profile)

    if broker == "replay":
        return RuntimePolicy(
            bot_name=bot_name,
            profile=args.profile,
            broker="sim-replay",
            market="sim-replay",
            venue="paper-sim",
            execution_mode="paper-sim",
        )

    if broker == "sim-forced":
        return RuntimePolicy(
            bot_name=bot_name,
            profile=args.profile,
            broker="sim-forced",
            market="sim-forced",
            venue="paper-sim",
            execution_mode="paper-sim",
        )

    if broker == "blofin-ws":
        return RuntimePolicy(
            bot_name=bot_name,
            profile=args.profile,
            broker="blofin-ws",
            market="blofin-ws",
            venue="blofin-demo",
            execution_mode=args.mode,
        )

    if broker == "oanda-practice":
        return RuntimePolicy(
            bot_name=bot_name,
            profile=args.profile,
            broker="oanda-practice",
            market="oanda-practice",
            venue="oanda-practice",
            execution_mode=args.mode,
        )

    if broker == "manual":
        return RuntimePolicy(
            bot_name=bot_name,
            profile=args.profile,
            broker="manual",
            market="yfinance",
            venue="manual",
            execution_mode=args.mode,
        )

    return RuntimePolicy(
        bot_name=bot_name,
        profile=args.profile,
        broker="yfinance",
        market="yfinance",
        venue="paper",
        execution_mode=args.mode,
    )


def load_local_module(module_basename: str):
    package_name = f"execute.{module_basename}"
    try:
        return importlib.import_module(package_name)
    except Exception:
        file_path = THIS_DIR / f"{module_basename}.py"
        if not file_path.exists():
            raise
        spec = importlib.util.spec_from_file_location(package_name, file_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load module from {file_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def load_legacy_runner():
    legacy_path = THIS_DIR / "custom_runtime_runner_orig.py"
    if not legacy_path.exists():
        raise RuntimeError(
            f"Missing legacy runner backup: {legacy_path}. "
            f"Create it first by copying the current runner to custom_runtime_runner_orig.py"
        )
    spec = importlib.util.spec_from_file_location("execute.custom_runtime_runner_orig", legacy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load legacy runner from {legacy_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def try_call(target: Any, variants: Iterable[tuple[tuple[Any, ...], dict[str, Any]]]) -> Any:
    last_exc: Optional[Exception] = None
    for args, kwargs in variants:
        try:
            return target(*args, **kwargs)
        except TypeError as exc:
            last_exc = exc
            continue
    if last_exc is not None:
        raise last_exc
    raise RuntimeError(f"No callable variants matched for {target}")


def make_engine_instance(engine_mod: Any, args: argparse.Namespace, policy: RuntimePolicy) -> Any:
    for cls_name in ("CustomLiveEngine", "LiveEngine", "GBLiveEngine"):
        cls = getattr(engine_mod, cls_name, None)
        if cls is None:
            continue

        ctor_variants = [
            ((args, policy), {}),
            ((args,), {}),
            ((), {"args": args, "policy": policy}),
            ((), {"policy": policy}),
            ((), {}),
        ]
        try:
            return try_call(cls, ctor_variants)
        except TypeError:
            continue
    return None


def normalize_signal(result: Any) -> Optional[dict]:
    if result is None:
        return None

    if isinstance(result, tuple):
        for item in result:
            if isinstance(item, dict):
                result = item
                break
        else:
            result = result[0]

    if isinstance(result, dict):
        if result.get("confirmed") is False:
            return None
        if result.get("status") == "none":
            return None
        if result.get("signal") is False:
            return None
        return dict(result)

    if hasattr(result, "__dict__"):
        payload = dict(vars(result))
        if payload.get("confirmed") is False:
            return None
        return payload

    return None


def evaluate_live_engine(window_df: Any, args: argparse.Namespace, policy: RuntimePolicy) -> Optional[dict]:
    engine_mod = load_local_module("custom_live_engine")

    fn_variants = [
        ("run_once", [
            ((window_df, args, policy), {}),
            ((window_df, policy), {}),
            ((window_df, args), {}),
            ((window_df,), {}),
            ((), {"window_df": window_df, "args": args, "policy": policy}),
            ((), {"df": window_df, "args": args, "policy": policy}),
            ((), {"df": window_df}),
        ]),
        ("evaluate_once", [
            ((window_df, args, policy), {}),
            ((window_df, policy), {}),
            ((window_df, args), {}),
            ((window_df,), {}),
            ((), {"df": window_df, "args": args, "policy": policy}),
        ]),
        ("process_window", [
            ((window_df, args, policy), {}),
            ((window_df, policy), {}),
            ((window_df,), {}),
            ((), {"df": window_df}),
        ]),
        ("generate_signal", [
            ((window_df, args, policy), {}),
            ((window_df, policy), {}),
            ((window_df,), {}),
        ]),
        ("get_confirmed_signal", [
            ((window_df, args, policy), {}),
            ((window_df, policy), {}),
            ((window_df,), {}),
        ]),
    ]

    for fn_name, variants in fn_variants:
        fn = getattr(engine_mod, fn_name, None)
        if callable(fn):
            try:
                return normalize_signal(try_call(fn, variants))
            except TypeError:
                pass

    engine_obj = make_engine_instance(engine_mod, args, policy)
    if engine_obj is not None:
        for method_name, variants in (
            ("run_once", [
                ((window_df,), {}),
                ((window_df, args, policy), {}),
                ((window_df, policy), {}),
                ((), {"df": window_df}),
            ]),
            ("evaluate_once", [
                ((window_df,), {}),
                ((window_df, args, policy), {}),
                ((window_df, policy), {}),
                ((), {"df": window_df}),
            ]),
            ("process_window", [
                ((window_df,), {}),
                ((window_df, args, policy), {}),
                ((window_df, policy), {}),
                ((), {"df": window_df}),
            ]),
            ("generate_signal", [
                ((window_df,), {}),
                ((window_df, args, policy), {}),
                ((window_df, policy), {}),
                ((), {"df": window_df}),
            ]),
            ("get_confirmed_signal", [
                ((window_df,), {}),
                ((window_df, args, policy), {}),
                ((window_df, policy), {}),
                ((), {"df": window_df}),
            ]),
        ):
            method = getattr(engine_obj, method_name, None)
            if callable(method):
                try:
                    return normalize_signal(try_call(method, variants))
                except TypeError:
                    pass

    raise RuntimeError(
        "Unable to find compatible custom_live_engine entrypoint. "
        "Update evaluate_live_engine() adapter to match your local signatures."
    )


def annotate_signal(signal: dict, args: argparse.Namespace, policy: RuntimePolicy, source: str) -> dict:
    payload = dict(signal)
    payload["bot_name"] = payload.get("bot_name", policy.bot_name)
    payload["profile"] = payload.get("profile", args.profile)
    payload["family"] = payload.get("family", args.family)
    payload["symbol"] = payload.get("symbol", args.symbol)
    payload["timeframe"] = payload.get("timeframe", args.timeframe)
    payload["broker"] = policy.broker
    payload["market"] = policy.market
    payload["venue"] = policy.venue
    payload["execution_mode"] = policy.execution_mode
    payload["simulated"] = True
    payload["signal_source"] = source
    return payload


def execute_paper_signal(signal: dict, args: argparse.Namespace, policy: RuntimePolicy, bar: Optional[dict] = None) -> Any:
    paper_mod = load_local_module("paper_executor")

    fn_variants = [
        ("execute_signal", [
            ((signal, args, policy), {}),
            ((signal, policy), {}),
            ((signal,), {}),
            ((), {"signal": signal, "args": args, "policy": policy, "bar": bar}),
            ((), {"signal": signal, "policy": policy, "bar": bar}),
            ((), {"signal": signal}),
        ]),
        ("execute", [
            ((signal, args, policy), {}),
            ((signal, policy), {}),
            ((signal,), {}),
            ((), {"signal": signal, "args": args, "policy": policy, "bar": bar}),
            ((), {"signal": signal, "policy": policy, "bar": bar}),
        ]),
        ("submit_paper_trade", [
            ((signal, args, policy), {}),
            ((signal, policy), {}),
            ((signal,), {}),
            ((), {"signal": signal, "policy": policy}),
        ]),
        ("handle_signal", [
            ((signal, args, policy), {}),
            ((signal, policy), {}),
            ((signal,), {}),
            ((), {"signal": signal, "policy": policy}),
        ]),
        ("record_signal", [
            ((signal, args, policy), {}),
            ((signal, policy), {}),
            ((signal,), {}),
            ((), {"signal": signal, "policy": policy}),
        ]),
    ]

    for fn_name, variants in fn_variants:
        fn = getattr(paper_mod, fn_name, None)
        if callable(fn):
            try:
                return try_call(fn, variants)
            except TypeError:
                pass

    for cls_name in ("PaperExecutor", "GBPaperExecutor"):
        cls = getattr(paper_mod, cls_name, None)
        if cls is None:
            continue

        ctor_variants = [
            ((args, policy), {}),
            ((policy,), {}),
            ((args,), {}),
            ((), {"args": args, "policy": policy}),
            ((), {"policy": policy}),
            ((), {}),
        ]
        try:
            executor_obj = try_call(cls, ctor_variants)
        except TypeError:
            continue

        for method_name, variants in (
            ("execute_signal", [
                ((signal,), {}),
                ((signal, bar), {}),
                ((signal, args, policy), {}),
                ((), {"signal": signal, "bar": bar}),
            ]),
            ("execute", [
                ((signal,), {}),
                ((signal, bar), {}),
                ((signal, args, policy), {}),
                ((), {"signal": signal, "bar": bar}),
            ]),
            ("submit_paper_trade", [
                ((signal,), {}),
                ((signal, bar), {}),
                ((), {"signal": signal, "bar": bar}),
            ]),
            ("handle_signal", [
                ((signal,), {}),
                ((signal, bar), {}),
                ((), {"signal": signal, "bar": bar}),
            ]),
            ("record_signal", [
                ((signal,), {}),
                ((signal, bar), {}),
                ((), {"signal": signal, "bar": bar}),
            ]),
        ):
            method = getattr(executor_obj, method_name, None)
            if callable(method):
                try:
                    return try_call(method, variants)
                except TypeError:
                    pass

    raise RuntimeError(
        "Unable to find compatible paper_executor entrypoint. "
        "Update execute_paper_signal() adapter to match your local signatures."
    )


def log_policy(args: argparse.Namespace, policy: RuntimePolicy) -> None:
    log.info(
        "Runtime policy | bot=%s family=%s symbol=%s tf=%s market=%s venue=%s mode=%s",
        policy.bot_name,
        args.family,
        args.symbol,
        args.timeframe,
        policy.market,
        policy.venue,
        policy.execution_mode,
    )


def run_replay(args: argparse.Namespace, policy: RuntimePolicy) -> None:
    feed = ReplayFeed(
        symbol=args.symbol,
        timeframe=args.timeframe,
        csv_path=args.replay_csv,
    )

    executed = 0
    checked = 0

    for window_df, bar in feed.iter_windows(seed_limit=args.seed_limit, max_events=args.max_events):
        checked += 1
        signal = evaluate_live_engine(window_df, args, policy)
        if signal:
            payload = annotate_signal(signal, args, policy, source="replay")
            execute_paper_signal(payload, args, policy, bar=bar)
            executed += 1
            log.info(
                "Replay executed | symbol=%s tf=%s broker=%s checked=%s executed=%s",
                args.symbol, args.timeframe, policy.broker, checked, executed
            )
            if args.once:
                return

        if args.interval and args.interval > 0:
            time.sleep(float(args.interval))

    if executed == 0:
        log.info(
            "Replay completed | no confirmed signal in last %s replay events.",
            args.max_events,
        )


def run_sim_forced(args: argparse.Namespace, policy: RuntimePolicy) -> None:
    price = 100.0
    try:
        price = ReplayFeed(
            symbol=args.symbol,
            timeframe=args.timeframe,
            csv_path=args.replay_csv,
        ).last_price()
    except Exception:
        pass

    payload = annotate_signal(
        build_forced_signal(args=args, policy=policy, price=price),
        args=args,
        policy=policy,
        source="sim-forced",
    )
    execute_paper_signal(payload, args, policy, bar={"close": price})
    log.info(
        "Sim-forced executed | symbol=%s tf=%s broker=%s entry=%s",
        args.symbol, args.timeframe, policy.broker, price
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True, choices=["cipher", "parallax", "combined"])
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--timeframe", default="15m")
    parser.add_argument("--profile", default="manual-signals")
    parser.add_argument(
        "--broker",
        required=True,
        choices=["auto", "yfinance", "blofin-ws", "oanda-practice", "manual", "replay", "sim-forced"],
    )
    parser.add_argument("--mode", default="paper", choices=["", "shadow", "paper"])
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=float, default=0.0)
    parser.add_argument("--seed-limit", type=int, default=300)
    parser.add_argument("--max-events", type=int, default=20)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--replay-csv", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.broker in LEGACY_BROKERS:
        legacy = load_legacy_runner()
        legacy.main()
        return

    policy = resolve_policy(args)
    log_policy(args, policy)

    if args.broker == "replay":
        run_replay(args, policy)
        return

    if args.broker == "sim-forced":
        run_sim_forced(args, policy)
        return

    raise RuntimeError(f"Unsupported broker dispatch: {args.broker}")


if __name__ == "__main__":
    main()