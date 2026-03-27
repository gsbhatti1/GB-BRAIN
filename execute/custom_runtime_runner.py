from __future__ import annotations

import argparse
import asyncio
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

def maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        try:
            return asyncio.run(value)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(value)
            finally:
                loop.close()
    return value


def _sig(obj: Any) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return "(signature unavailable)"


def _last_bar_from_window(window_df: Any) -> Optional[dict]:
    try:
        if window_df is None or len(window_df) == 0:
            return None
        if hasattr(window_df, "iloc"):
            row = window_df.iloc[-1]
            if hasattr(row, "to_dict"):
                return dict(row.to_dict())
        return None
    except Exception:
        return None


def _resolve_param(name: str, context: dict[str, Any]) -> tuple[bool, Any]:
    lname = name.lower()

    if lname in context:
        return True, context[lname]

    if lname in {"args", "cli_args", "options", "config", "cfg", "params"}:
        return True, context.get("args")

    if "policy" in lname:
        return True, context.get("policy")

    if lname in {"signal", "payload", "trade", "order"} or "signal" in lname:
        return True, context.get("signal")

    if lname in {"bar", "candle", "tick", "latest_bar", "latest_candle", "last_bar", "last_candle"}:
        return True, context.get("bar")

    if lname in {
        "df", "data", "window", "window_df", "dataframe", "bars", "candles",
        "history", "price_df", "market_df", "ohlc", "ohlcv"
    }:
        return True, context.get("window_df")

    if "window" in lname or "candle" in lname or "bar" in lname or "ohlc" in lname:
        return True, context.get("window_df")

    if lname == "symbol":
        return True, context.get("symbol")

    if lname == "timeframe":
        return True, context.get("timeframe")

    if lname == "family":
        return True, context.get("family")

    if lname == "profile":
        return True, context.get("profile")

    if lname == "broker":
        return True, context.get("broker")

    if lname == "execution_mode":
        return True, context.get("execution_mode")

    if lname == "bot_name":
        return True, context.get("bot_name")

    return False, None


def _bind_for_call(target: Any, context: dict[str, Any]) -> tuple[list[Any], dict[str, Any]]:
    sig = inspect.signature(target)
    pos_args: list[Any] = []
    kw_args: dict[str, Any] = {}

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        found, value = _resolve_param(name, context)

        if not found:
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.default is inspect._empty:
                raise TypeError(f"unresolved required param: {name}")
            continue

        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            pos_args.append(value)
        elif param.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            kw_args[name] = value
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            continue

    return pos_args, kw_args


def _call_bound(target: Any, context: dict[str, Any]) -> Any:
    pos_args, kw_args = _bind_for_call(target, context)
    return maybe_await(target(*pos_args, **kw_args))


def _public_functions(module: Any) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            out.append((name, obj))
    return out


def _public_classes(module: Any) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        if inspect.isclass(obj) and getattr(obj, "__module__", "") == getattr(module, "__name__", ""):
            out.append((name, obj))
    return out


def _callable_score(name: str, exact_names: list[str], keywords: list[str]) -> int:
    lname = name.lower()
    score = 0
    if lname in {x.lower() for x in exact_names}:
        score += 100
    for kw in keywords:
        if kw in lname:
            score += 10
    return score


def _module_debug_dump(module: Any) -> str:
    lines: list[str] = []
    lines.append(f"MODULE {getattr(module, '__name__', '<unknown>')}")
    lines.append("FUNCTIONS:")
    for name, fn in _public_functions(module):
        lines.append(f"  - {name}{_sig(fn)}")
    lines.append("CLASSES:")
    for name, cls in _public_classes(module):
        lines.append(f"  - {name}{_sig(cls)}")
        try:
            method_lines = []
            for m_name, m_obj in inspect.getmembers(cls):
                if m_name.startswith("_") and m_name != "__call__":
                    continue
                if callable(m_obj):
                    method_lines.append(f"      * {m_name}{_sig(m_obj)}")
            lines.extend(method_lines[:40])
        except Exception:
            pass
    return "\n".join(lines)


def _normalize_signal(result: Any) -> Optional[dict]:
    if result is None:
        return None

    if isinstance(result, dict):
        if "signal" in result and isinstance(result["signal"], dict):
            result = result["signal"]
        if result.get("confirmed") is False:
            return None
        if result.get("status") in {"none", "no_signal"}:
            return None
        if result.get("signal") is False:
            return None
        return dict(result)

    if isinstance(result, (tuple, list)):
        for item in result:
            normalized = _normalize_signal(item)
            if normalized:
                return normalized
        return None

    if hasattr(result, "to_dict"):
        try:
            return _normalize_signal(result.to_dict())
        except Exception:
            pass

    if hasattr(result, "__dict__"):
        try:
            payload = dict(vars(result))
            if payload.get("confirmed") is False:
                return None
            return payload
        except Exception:
            pass

    return None


def _instantiate_best_class(module: Any, context: dict[str, Any], exact_names: list[str], keywords: list[str]) -> Any:
    candidates = []
    for name, cls in _public_classes(module):
        score = _callable_score(name, exact_names, keywords)
        if score > 0:
            candidates.append((score, name, cls))

    candidates.sort(key=lambda x: (-x[0], x[1]))

    for _, _, cls in candidates:
        try:
            return _call_bound(cls, context)
        except TypeError:
            continue

    return None


def _run_named_functions(module: Any, context: dict[str, Any], names: list[str]) -> tuple[bool, Any]:
    fn_map = {name.lower(): obj for name, obj in _public_functions(module)}
    for name in names:
        fn = fn_map.get(name.lower())
        if fn is None:
            continue
        try:
            return True, _call_bound(fn, context)
        except TypeError:
            continue
    return False, None


def _run_named_methods(obj: Any, context: dict[str, Any], names: list[str]) -> tuple[bool, Any]:
    for name in names:
        method = getattr(obj, name, None)
        if callable(method):
            try:
                return True, _call_bound(method, context)
            except TypeError:
                continue
    return False, None


def _run_scored_functions(module: Any, context: dict[str, Any], exact_names: list[str], keywords: list[str]) -> tuple[bool, Any]:
    candidates = []
    for name, fn in _public_functions(module):
        score = _callable_score(name, exact_names, keywords)
        if score > 0:
            candidates.append((score, name, fn))

    candidates.sort(key=lambda x: (-x[0], x[1]))

    for _, _, fn in candidates:
        try:
            return True, _call_bound(fn, context)
        except TypeError:
            continue

    return False, None


def _run_scored_methods(obj: Any, context: dict[str, Any], exact_names: list[str], keywords: list[str]) -> tuple[bool, Any]:
    candidates = []
    for name, member in inspect.getmembers(obj):
        if name.startswith("_") and name != "__call__":
            continue
        if not callable(member):
            continue
        score = _callable_score(name, exact_names, keywords)
        if score > 0:
            candidates.append((score, name, member))

    candidates.sort(key=lambda x: (-x[0], x[1]))

    for _, _, method in candidates:
        try:
            return True, _call_bound(method, context)
        except TypeError:
            continue

    return False, None


def evaluate_live_engine(window_df: Any, args: argparse.Namespace, policy: RuntimePolicy) -> Optional[dict]:
    engine_mod = load_local_module("custom_live_engine")
    bar = _last_bar_from_window(window_df)

    context = {
        "args": args,
        "policy": policy,
        "window_df": window_df,
        "bar": bar,
        "signal": None,
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "family": args.family,
        "profile": args.profile,
        "broker": policy.broker,
        "execution_mode": policy.execution_mode,
        "bot_name": policy.bot_name,
    }

    exact_fn_names = [
        "run_once",
        "evaluate_once",
        "process_window",
        "generate_signal",
        "get_confirmed_signal",
        "on_bar",
        "on_candle",
        "handle_bar",
        "handle_candle",
        "step",
        "process",
        "evaluate",
        "run",
        "__call__",
    ]
    keywords = ["signal", "evaluate", "process", "handle", "run", "bar", "candle", "engine", "live", "confirm"]

    matched, result = _run_named_functions(engine_mod, context, exact_fn_names)
    if matched:
        return _normalize_signal(result)

    matched, result = _run_scored_functions(engine_mod, context, exact_fn_names, keywords)
    if matched:
        return _normalize_signal(result)

    engine_obj = _instantiate_best_class(
        engine_mod,
        context,
        exact_names=["customliveengine", "liveengine", "gbliveengine", "engine", "runner", "processor"],
        keywords=["engine", "runner", "processor", "live", "strategy"],
    )

    if engine_obj is not None:
        matched, result = _run_named_methods(engine_obj, context, exact_fn_names)
        if matched:
            return _normalize_signal(result)

        matched, result = _run_scored_methods(engine_obj, context, exact_fn_names, keywords)
        if matched:
            return _normalize_signal(result)

    raise RuntimeError(
        "Unable to find compatible custom_live_engine entrypoint.\n\n"
        + _module_debug_dump(engine_mod)
    )


def execute_paper_signal(signal: dict, args: argparse.Namespace, policy: RuntimePolicy, bar: Optional[dict] = None) -> Any:
    paper_mod = load_local_module("paper_executor")

    context = {
        "args": args,
        "policy": policy,
        "window_df": None,
        "bar": bar,
        "signal": signal,
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "family": args.family,
        "profile": args.profile,
        "broker": policy.broker,
        "execution_mode": policy.execution_mode,
        "bot_name": policy.bot_name,
    }

    exact_fn_names = [
        "execute_signal",
        "execute",
        "submit_paper_trade",
        "handle_signal",
        "record_signal",
        "record_execution",
        "persist_signal",
        "write_signal",
        "process_signal",
        "on_signal",
        "__call__",
    ]
    keywords = ["execute", "submit", "handle", "record", "persist", "write", "paper", "signal", "trade", "order"]

    matched, result = _run_named_functions(paper_mod, context, exact_fn_names)
    if matched:
        return result

    matched, result = _run_scored_functions(paper_mod, context, exact_fn_names, keywords)
    if matched:
        return result

    paper_obj = _instantiate_best_class(
        paper_mod,
        context,
        exact_names=["paperexecutor", "gbpaperexecutor", "executor", "papertrader", "paperbroker"],
        keywords=["executor", "paper", "broker", "trader"],
    )

    if paper_obj is not None:
        matched, result = _run_named_methods(paper_obj, context, exact_fn_names)
        if matched:
            return result

        matched, result = _run_scored_methods(paper_obj, context, exact_fn_names, keywords)
        if matched:
            return result

    raise RuntimeError(
        "Unable to find compatible paper_executor entrypoint.\n\n"
        + _module_debug_dump(paper_mod)
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