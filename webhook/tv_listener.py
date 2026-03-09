"""
GB-BRAIN - TradingView Webhook Listener
=========================================
Receives webhook alerts from TradingView, validates them,
and routes orders to the correct broker.

Usage:
    python webhook/tv_listener.py

TradingView alert format (JSON):
{
    "secret": "your_webhook_secret",
    "symbol": "ETHUSDT",
    "side": "buy",
    "units": 0.1,
    "broker": "blofin"
}
"""

import sys
import logging
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, request, jsonify

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import TV_SECRET, TV_PORT
from execute.risk_manager import RiskManager
from execute.telegram_alerts import send_alert, send_trade_alert, send_error

logger = logging.getLogger("gb_brain.webhook")

app = Flask(__name__)
risk = RiskManager()

# Trade counter per day
_trade_counts = {}
MAX_TRADES_PER_DAY = 20


def _today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _get_broker(name):
    """Get the right broker bridge."""
    if name == "oanda":
        from execute.oanda_bridge import place_order, get_account_balance
        return place_order, get_account_balance
    elif name == "blofin":
        from execute.blofin_bridge import BloFinBridge
        bridge = BloFinBridge(use_demo=True)
        return bridge.place_order, bridge.get_balance
    else:
        raise ValueError(f"Unknown broker: {name}")


@app.route("/webhook", methods=["POST"])
def webhook():
    """Main webhook endpoint for TradingView alerts."""
    if not request.is_json:
        return jsonify({"ok": False, "error": "Expected JSON"}), 400

    data = request.get_json(silent=True) or {}

    # Validate secret
    if data.get("secret") != TV_SECRET:
        send_alert("Webhook: invalid secret received")
        return jsonify({"ok": False, "error": "Invalid secret"}), 401

    # Parse signal
    symbol = str(data.get("symbol", "")).strip()
    side = str(data.get("side", "")).lower().strip()
    units = float(data.get("units", 0))
    broker = str(data.get("broker", "oanda")).lower().strip()

    if side not in ("buy", "sell"):
        return jsonify({"ok": False, "error": f"Invalid side: {side}"}), 400
    if not symbol:
        return jsonify({"ok": False, "error": "Missing symbol"}), 400
    if units <= 0:
        return jsonify({"ok": False, "error": f"Invalid units: {units}"}), 400

    # Daily trade limit
    today = _today()
    _trade_counts.setdefault(today, 0)
    if _trade_counts[today] >= MAX_TRADES_PER_DAY:
        send_alert(f"Webhook blocked: daily limit ({MAX_TRADES_PER_DAY})")
        return jsonify({"ok": False, "error": "Daily trade limit"}), 403

    # Risk check
    can, reason = risk.can_trade()
    if not can:
        send_alert(f"Webhook blocked by risk: {reason}")
        return jsonify({"ok": False, "error": reason}), 403

    # Execute
    try:
        place_fn, _ = _get_broker(broker)
        if broker == "oanda":
            order_units = int(units) if side == "buy" else -int(units)
            result = place_fn(symbol, order_units, tag="GB-BRAIN-TV")
        elif broker == "blofin":
            result = place_fn(symbol, side, units)
        else:
            result = place_fn(symbol, units)

        _trade_counts[today] += 1
        send_trade_alert("fill", symbol, side, units)
        return jsonify({"ok": True, "result": str(result)}), 200

    except Exception as e:
        send_error(f"webhook_{broker}", e)
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
        "risk": risk.report(),
        "trades_today": _trade_counts.get(_today(), 0),
    }), 200


@app.route("/risk", methods=["GET"])
def risk_status():
    return jsonify({
        "report": risk.report(),
        "can_trade": risk.can_trade()[0],
        "reason": risk.can_trade()[1],
    }), 200


@app.route("/kill", methods=["POST"])
def kill_switch():
    """Emergency stop all trading."""
    risk.state.is_halted = True
    risk.state.halt_reason = "Manual kill switch activated"
    send_alert("KILL SWITCH ACTIVATED - all trading stopped")
    return jsonify({"ok": True, "message": "Trading halted"}), 200


if __name__ == "__main__":
    print(f"GB-BRAIN Webhook Listener starting on port {TV_PORT}")
    print(f"Endpoints:")
    print(f"  POST /webhook  - TradingView alerts")
    print(f"  GET  /health   - Health check")
    print(f"  GET  /risk     - Risk status")
    print(f"  POST /kill     - Emergency stop")
    app.run(host="0.0.0.0", port=TV_PORT)
