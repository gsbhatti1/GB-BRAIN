# patch_alpaca_demo.py -- add Alpaca broker support to demo_runner.py
# Run from /home/gb-brain/GB-BRAIN
from pathlib import Path

target = Path("runtime/demo_runner.py")
src = target.read_text(encoding="utf-8")
original = src

# 1. Add alpaca to VALID_BROKERS and symbol sets
src = src.replace(
    'BLOFIN_SYMBOLS = {"ETH", "BTC", "SOL"}\nOANDA_SYMBOLS  = {"NAS100", "US30", "SPX500"}\nVALID_BROKERS  = {"blofin", "oanda"}',
    'BLOFIN_SYMBOLS  = {"ETH", "BTC", "SOL"}\nOANDA_SYMBOLS   = {"NAS100", "US30", "SPX500"}\nALPACA_SYMBOLS  = {"^GSPC", "SPY", "QQQ", "AAPL", "TSLA"}\nVALID_BROKERS   = {"blofin", "oanda", "alpaca"}'
)

# 2. Add alpaca import function after _import_oanda_bridge
ALPACA_IMPORT = '''

def _import_alpaca_bridge():
    try:
        import execute.alpaca_bridge as _ab
        class AlpacaBridge:
            def get_latest_candle(self, symbol, timeframe):
                try:
                    price = _ab.get_price(symbol)
                except Exception:
                    price = None
                if price is None:
                    return None
                return {"open": price, "high": price, "low": price,
                        "close": price, "volume": 0}
            def place_order(self, symbol=None, side="BUY", size=1, order_type="market", **kw):
                try:
                    qty = size if side == "BUY" else -abs(size)
                    return _ab.place_order(symbol, qty)
                except Exception as exc:
                    logger.error("Alpaca order error: %s", exc)
                    return None
        return AlpacaBridge
    except ImportError as exc:
        logger.warning("AlpacaBridge not found: %s", exc)
        return None
'''

src = src.replace(
    "\ndef _import_engine():",
    ALPACA_IMPORT + "\ndef _import_engine():"
)

# 3. Add alpaca lane name in __init__
src = src.replace(
    'self._lane_name = "GB-INDICES" if broker == "oanda" else "GB-CRYPTO-BOT"',
    'if broker == "oanda":\n            self._lane_name = "GB-INDICES"\n        elif broker == "alpaca":\n            self._lane_name = "GB-INDICES"\n        else:\n            self._lane_name = "GB-CRYPTO-BOT"'
)

# 4. Wire alpaca bridge in _init_components
src = src.replace(
    '        # Broker bridge\n        if self.broker == "blofin":\n            BF = _import_blofin_bridge()\n            if BF:\n                self._bridge = BF()\n        else:\n            OA = _import_oanda_bridge()\n            if OA:\n                self._bridge = OA()',
    '        # Broker bridge\n        if self.broker == "blofin":\n            BF = _import_blofin_bridge()\n            if BF:\n                self._bridge = BF()\n        elif self.broker == "alpaca":\n            AB = _import_alpaca_bridge()\n            if AB:\n                self._bridge = AB()\n        else:\n            OA = _import_oanda_bridge()\n            if OA:\n                self._bridge = OA()'
)

# 5. Fix place_order routing for alpaca
src = src.replace(
    '        try:\n            if self.broker == "blofin":\n                result = self._bridge.place_order(\n                    symbol=self.symbol,\n                    side=side,\n                    size=units,\n                    order_type="market",\n                )\n            else:  # oanda\n                result = self._bridge.place_order(\n                    instrument=self.symbol,\n                    units=units if side == "BUY" else -abs(units),\n                )\n            return result',
    '        try:\n            if self.broker == "blofin":\n                result = self._bridge.place_order(\n                    symbol=self.symbol,\n                    side=side,\n                    size=units,\n                    order_type="market",\n                )\n            elif self.broker == "alpaca":\n                result = self._bridge.place_order(\n                    symbol=self.symbol,\n                    side=side,\n                    size=units,\n                )\n            else:  # oanda\n                result = self._bridge.place_order(\n                    instrument=self.symbol,\n                    units=units if side == "BUY" else -abs(units),\n                )\n            return result'
)

# 6. Add alpaca to list_demo_accounts
src = src.replace(
    '    print(f"  BloFin demo    — symbols: {sorted(BLOFIN_SYMBOLS)}")\n    print(f"  OANDA practice — symbols: {sorted(OANDA_SYMBOLS)}")',
    '    print(f"  BloFin demo    — symbols: {sorted(BLOFIN_SYMBOLS)}")\n    print(f"  OANDA practice — symbols: {sorted(OANDA_SYMBOLS)}")\n    print(f"  Alpaca paper   — symbols: {sorted(ALPACA_SYMBOLS)}")'
)

if src != original:
    target.write_text(src, encoding="utf-8")
    changes = sum([
        'alpaca' in src,
        'AlpacaBridge' in src,
        'ALPACA_SYMBOLS' in src,
    ])
    print(f"OK — demo_runner.py patched with Alpaca support ({changes}/3 sections confirmed)")
else:
    print("ERROR — no changes made, patterns not found")
    print("Check demo_runner.py manually")
