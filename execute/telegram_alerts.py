"""
GB-BRAIN — Telegram Alerts
============================
Send notifications for trades, errors, and daily summaries.

Usage:
    from execute.telegram_alerts import send_alert, send_trade_alert
"""

import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT


def send_alert(message, parse_mode="HTML"):
    """Send a Telegram message. Returns True on success."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        print(f"[TELEGRAM] (disabled) {message[:80]}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT,
            "text": message,
            "parse_mode": parse_mode,
        }, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False


def send_trade_alert(action, symbol, side, units, price=None, pnl=None):
    """Send a formatted trade notification."""
    icon = "✅" if action == "fill" else "❌" if action == "error" else "⚠️"
    msg = f"{icon} <b>{action.upper()}</b>\n"
    msg += f"  Symbol: <code>{symbol}</code>\n"
    msg += f"  Side: <code>{side}</code>\n"
    msg += f"  Units: <code>{units}</code>\n"
    if price:
        msg += f"  Price: <code>{price}</code>\n"
    if pnl is not None:
        emoji = "📈" if pnl > 0 else "📉"
        msg += f"  PnL: {emoji} <code>{pnl:+.2f}</code>\n"
    return send_alert(msg)


def send_daily_summary(stats):
    """Send end-of-day summary."""
    msg = "📊 <b>Daily Summary</b>\n"
    msg += f"  Trades: {stats.get('trades', 0)}\n"
    msg += f"  Wins: {stats.get('wins', 0)}\n"
    msg += f"  Losses: {stats.get('losses', 0)}\n"
    msg += f"  P&L: <code>{stats.get('pnl', 0):+.2f}</code>\n"
    msg += f"  Balance: <code>{stats.get('balance', 0):.2f}</code>"
    return send_alert(msg)


def send_error(context, error):
    """Send error notification."""
    msg = f"🚨 <b>ERROR</b>\n"
    msg += f"  Context: <code>{context}</code>\n"
    msg += f"  Error: <code>{str(error)[:200]}</code>"
    return send_alert(msg)


if __name__ == "__main__":
    send_alert("🧠 GB-BRAIN — Telegram alerts connected!")
