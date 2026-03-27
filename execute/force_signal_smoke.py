from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def build_forced_signal(args: Any, policy: Any, price: float, side: str = "long") -> Dict[str, Any]:
    price = float(price)

    if side.lower() == "short":
        stop = round(price * 1.01, 8)
        tp1 = round(price * 0.99, 8)
        tp2 = round(price * 0.985, 8)
        tp3 = round(price * 0.98, 8)
    else:
        stop = round(price * 0.99, 8)
        tp1 = round(price * 1.01, 8)
        tp2 = round(price * 1.015, 8)
        tp3 = round(price * 1.02, 8)

    ts = datetime.now(timezone.utc).isoformat()

    return {
        "signal_id": f"sim-forced-{args.symbol}-{args.timeframe}-{int(datetime.now(timezone.utc).timestamp())}",
        "timestamp": ts,
        "bot_name": getattr(policy, "bot_name", getattr(args, "profile", "GB-BRAIN")),
        "profile": getattr(args, "profile", "unknown"),
        "family": args.family,
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "side": side.lower(),
        "status": "confirmed",
        "signal_state": "confirmed",
        "confirmed": True,
        "score": 100.0,
        "confidence": 1.0,
        "entry": price,
        "entry_price": price,
        "stop": stop,
        "stop_price": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "reason": "phase2d_sim_forced_smoke",
        "notes": "synthetic smoke signal for PC runtime path; not valid for performance analytics",
        "simulated": True,
    }