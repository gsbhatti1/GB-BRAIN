"""
GB-BRAIN - OANDA Bridge
=========================
Executes trades on OANDA for indices (NAS100, US30, SPX500).
Supports demo and live accounts.
"""

import sys
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import OANDA_ACCOUNT, OANDA_TOKEN, OANDA_URL

logger = logging.getLogger("gb_brain.oanda")

# OANDA instrument mapping
SYMBOL_MAP = {
    "NAS100": "NAS100_USD",
    "US30":   "US30_USD",
    "SPX500": "SPX500_USD",
    "SPX":    "SPX500_USD",
    "^NDX":   "NAS100_USD",
    "^DJI":   "US30_USD",
    "^GSPC":  "SPX500_USD",
}


def _get_client():
    """Create OANDA API client."""
    import oandapyV20
    env = "practice" if "practice" in OANDA_URL else "live"
    return oandapyV20.API(access_token=OANDA_TOKEN, environment=env)


def _resolve_instrument(symbol):
    """Convert our symbol to OANDA instrument name."""
    return SYMBOL_MAP.get(symbol, symbol)


def place_order(symbol, units, tag="GB-BRAIN"):
    """Place a market order. Positive units=long, negative=short."""
    import oandapyV20.endpoints.orders as ep
    client = _get_client()
    instrument = _resolve_instrument(symbol)

    data = {
        "order": {
            "instrument": instrument,
            "units": str(int(units)),
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "clientExtensions": {"tag": tag},
        }
    }

    r = ep.OrderCreate(accountID=OANDA_ACCOUNT, data=data)
    client.request(r)
    logger.info(f"OANDA order: {instrument} {units} units | {r.response}")
    return r.response


def close_position(symbol):
    """Close all positions for an instrument."""
    import oandapyV20.endpoints.positions as ep
    client = _get_client()
    instrument = _resolve_instrument(symbol)

    data = {"longUnits": "ALL", "shortUnits": "ALL"}
    r = ep.PositionClose(accountID=OANDA_ACCOUNT, instrument=instrument, data=data)
    try:
        client.request(r)
        logger.info(f"OANDA closed: {instrument}")
        return r.response
    except Exception as e:
        logger.warning(f"OANDA close failed: {e}")
        return None


def get_position(symbol):
    """Get current position for an instrument. Returns net units."""
    import oandapyV20.endpoints.positions as ep
    client = _get_client()
    instrument = _resolve_instrument(symbol)

    r = ep.PositionDetails(accountID=OANDA_ACCOUNT, instrument=instrument)
    try:
        client.request(r)
        pos = r.response["position"]
        long_u = int(pos["long"]["units"])
        short_u = int(pos["short"]["units"])
        return long_u + short_u
    except Exception:
        return 0


def get_account_balance():
    """Get account NAV and P&L."""
    import oandapyV20.endpoints.accounts as ep
    client = _get_client()

    r = ep.AccountDetails(accountID=OANDA_ACCOUNT)
    client.request(r)
    acc = r.response["account"]
    nav = float(acc["NAV"])
    pnl = float(acc["pl"]) + float(acc.get("unrealizedPL", "0"))
    return {"nav": nav, "pnl": pnl, "balance": float(acc["balance"])}


def get_price(symbol):
    """Get current bid/ask price."""
    import oandapyV20.endpoints.pricing as ep
    client = _get_client()
    instrument = _resolve_instrument(symbol)

    params = {"instruments": instrument}
    r = ep.PricingInfo(accountID=OANDA_ACCOUNT, params=params)
    client.request(r)
    price = r.response["prices"][0]
    return {
        "bid": float(price["bids"][0]["price"]),
        "ask": float(price["asks"][0]["price"]),
        "mid": (float(price["bids"][0]["price"]) + float(price["asks"][0]["price"])) / 2,
    }


def test_connection():
    """Test OANDA connection."""
    try:
        info = get_account_balance()
        logger.info(f"OANDA connected: NAV=${info['nav']:.2f}")
        return True, info
    except Exception as e:
        logger.error(f"OANDA connection failed: {e}")
        return False, str(e)
