"""
GB-BRAIN - BloFin Bridge
==========================
Executes trades on BloFin for crypto futures (ETH, BTC, SOL).
Ported from PhantomFlip. Supports demo and live.
"""

import sys
import time
import hmac
import hashlib
import base64
import json
import logging
import math
from uuid import uuid4
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import BLOFIN_KEY, BLOFIN_SECRET, BLOFIN_PASS

logger = logging.getLogger("gb_brain.blofin")

DEMO_BASE = "https://demo-trading-openapi.blofin.com"
LIVE_BASE = "https://openapi.blofin.com"

# Symbol mapping
SYMBOL_MAP = {
    "ETHUSDT": "ETH-USDT",
    "BTCUSDT": "BTC-USDT",
    "SOLUSDT": "SOL-USDT",
    "ETH": "ETH-USDT",
    "BTC": "BTC-USDT",
    "SOL": "SOL-USDT",
}


class BloFinBridge:
    """BloFin futures trading bridge."""

    def __init__(self, use_demo=True):
        self.base_url = DEMO_BASE if use_demo else LIVE_BASE
        self.session = requests.Session()
        self.use_demo = use_demo

    def _sign(self, method, path, body=None):
        ts = str(int(datetime.now().timestamp() * 1000))
        nonce = str(uuid4())
        prehash = f"{path}{method}{ts}{nonce}"
        if body:
            prehash += json.dumps(body)
        hex_sig = hmac.new(
            BLOFIN_SECRET.encode(), prehash.encode(), hashlib.sha256
        ).hexdigest().encode()
        signature = base64.b64encode(hex_sig).decode()
        return {
            "ACCESS-KEY": BLOFIN_KEY,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": ts,
            "ACCESS-NONCE": nonce,
            "ACCESS-PASSPHRASE": BLOFIN_PASS,
            "Content-Type": "application/json",
        }

    def _get(self, path, params=None):
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items() if v)
            full_path = f"{path}?{query}" if query else path
        else:
            full_path = path
        headers = self._sign("GET", full_path)
        try:
            r = self.session.get(f"{self.base_url}{full_path}", headers=headers, timeout=10)
            data = r.json()
            if data.get("code") != "0":
                logger.error(f"BloFin GET {path}: {data}")
            return data
        except Exception as e:
            logger.error(f"BloFin GET failed: {e}")
            return {"code": "-1", "data": []}

    def _post(self, path, body):
        headers = self._sign("POST", path, body)
        try:
            r = self.session.post(f"{self.base_url}{path}", headers=headers, json=body, timeout=10)
            data = r.json()
            if data.get("code") != "0":
                logger.error(f"BloFin POST {path}: {data}")
            return data
        except Exception as e:
            logger.error(f"BloFin POST failed: {e}")
            return {"code": "-1", "data": []}

    @staticmethod
    def _resolve(symbol):
        return SYMBOL_MAP.get(symbol, symbol)

    def set_leverage(self, symbol, leverage=3, margin_mode="isolated"):
        inst = self._resolve(symbol)
        body = {
            "instId": inst,
            "leverage": str(leverage),
            "marginMode": margin_mode,
        }
        return self._post("/api/v1/account/set-leverage", body)

    def place_order(self, symbol, side, size, leverage=3, order_type="market"):
        """Place a futures order. side='buy' or 'sell'."""
        inst = self._resolve(symbol)
        self.set_leverage(symbol, leverage)

        body = {
            "instId": inst,
            "marginMode": "isolated",
            "side": side,
            "orderType": order_type,
            "size": str(size),
            "tradeSide": "open",
        }
        result = self._post("/api/v1/trade/order", body)
        logger.info(f"BloFin order: {inst} {side} {size} | {result}")
        return result

    def close_position(self, symbol, side="buy"):
        """Close a position."""
        inst = self._resolve(symbol)
        body = {
            "instId": inst,
            "marginMode": "isolated",
            "side": side,
            "tradeSide": "close",
        }
        return self._post("/api/v1/trade/close-position", body)

    def get_position(self, symbol=None):
        """Get current positions."""
        params = {}
        if symbol:
            params["instId"] = self._resolve(symbol)
        result = self._get("/api/v1/account/positions", params)
        return result.get("data", [])

    def get_balance(self):
        """Get account balance."""
        result = self._get("/api/v1/account/balance")
        data = result.get("data", [{}])
        if data:
            return {
                "equity": float(data[0].get("totalEquity", 0)),
                "available": float(data[0].get("availableBalance", 0)),
                "pnl": float(data[0].get("unrealizedPnl", 0)),
            }
        return {"equity": 0, "available": 0, "pnl": 0}

    def get_price(self, symbol):
        """Get last price for a symbol."""
        inst = self._resolve(symbol)
        result = self._get("/api/v1/market/ticker", {"instId": inst})
        data = result.get("data", [{}])
        if data:
            return float(data[0].get("lastPrice", 0))
        return 0.0

    def test_connection(self):
        """Test BloFin connection."""
        try:
            balance = self.get_balance()
            logger.info(f"BloFin connected: equity=${balance['equity']:.2f}")
            return True, balance
        except Exception as e:
            logger.error(f"BloFin connection failed: {e}")
            return False, str(e)
