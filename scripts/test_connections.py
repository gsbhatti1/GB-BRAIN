"""
GB-BRAIN - Test All Connections
================================
Tests connectivity to all configured brokers and services.

Usage:
    python scripts/test_connections.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def test_oanda():
    print("\n--- OANDA ---")
    try:
        from execute.oanda_bridge import test_connection
        ok, info = test_connection()
        if ok:
            print(f"  [OK] Connected | NAV: ${info['nav']:.2f} | PnL: ${info['pnl']:.2f}")
        else:
            print(f"  [FAIL] {info}")
        return ok
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_blofin():
    print("\n--- BloFin ---")
    try:
        from execute.blofin_bridge import BloFinBridge
        bridge = BloFinBridge(use_demo=True)
        ok, info = bridge.test_connection()
        if ok:
            print(f"  [OK] Connected | Equity: ${info['equity']:.2f}")
        else:
            print(f"  [FAIL] {info}")
        return ok
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_binance():
    print("\n--- Binance ---")
    try:
        from binance.client import Client
        from config.settings import BINANCE_KEY, BINANCE_SECRET
        client = Client(BINANCE_KEY, BINANCE_SECRET)
        info = client.get_account()
        balances = [b for b in info["balances"] if float(b["free"]) > 0]
        print(f"  [OK] Connected | {len(balances)} assets with balance")
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_telegram():
    print("\n--- Telegram ---")
    try:
        from execute.telegram_alerts import send_alert
        from config.settings import TELEGRAM_TOKEN
        if not TELEGRAM_TOKEN:
            print("  [SKIP] No token configured")
            return False
        ok = send_alert("GB-BRAIN connection test")
        print(f"  [{'OK' if ok else 'FAIL'}] Message {'sent' if ok else 'failed'}")
        return ok
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_database():
    print("\n--- Database ---")
    try:
        from db.brain_db import connect, get_stats
        conn = connect()
        stats = get_stats(conn)
        conn.close()
        print(f"  [OK] {stats['total_strategies']:,} strategies | "
              f"{stats['total_backtests']:,} backtests | {stats['gems']} GEMs")
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("GB-BRAIN - Connection Test")
    print("=" * 50)

    results = {
        "Database": test_database(),
        "OANDA": test_oanda(),
        "BloFin": test_blofin(),
        "Binance": test_binance(),
        "Telegram": test_telegram(),
    }

    print(f"\n{'=' * 50}")
    print("SUMMARY")
    for name, ok in results.items():
        icon = "[OK]  " if ok else "[FAIL]"
        print(f"  {icon} {name}")
    print(f"{'=' * 50}")
