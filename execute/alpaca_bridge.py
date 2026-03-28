"""
alpaca_bridge.py — GB-BRAIN Alpaca Broker Bridge
=================================================
Handles all Alpaca REST API interactions for US stocks and indices.
Uses alpaca-py (the official modern Alpaca SDK).

Supported symbols: SPY, QQQ, DIA, NVDA (and any valid Alpaca ticker).
Controlled via ALPACA_BASE_URL in config.settings:
  - Paper:  https://paper-api.alpaca.markets
  - Live:   https://api.alpaca.markets

Conventions:
  - SQLite is truth — fills recorded externally by order_tracker.
  - Capital is priority — never place orders without risk gate approval.
  - STOP → Backup → Patch → Run → Verify.
  - .env for secrets — NEVER commit API keys.
  - Deterministic — same inputs produce same order parameters.

Author: GB-BRAIN
Last Updated: 2026-03-28
"""

import logging
import time
from typing import Optional

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from config import settings

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.alpaca")

# ---------------------------------------------------------------------------
# Symbol mapping
# ---------------------------------------------------------------------------
SYMBOL_MAP: dict[str, str] = {
    "SPY":    "SPY",
    "QQQ":    "QQQ",
    "DIA":    "DIA",
    "NVDA":   "NVDA",
    "AAPL":   "AAPL",
    "MSFT":   "MSFT",
    "TSLA":   "TSLA",
    "AMZN":   "AMZN",
    "GOOGL":  "GOOGL",
    "META":   "META",
    "AMD":    "AMD",
    "COIN":   "COIN",
    "SPX":    "SPY",    # Route to SPY proxy
    "NAS100": "QQQ",    # Route to QQQ proxy
    "US30":   "DIA",    # Route to DIA proxy
    "ARKK":   "ARKK",
    "GLD":    "GLD",
    "SLV":    "SLV",
    "TLT":    "TLT",
    "IWM":    "IWM",
}

# ---------------------------------------------------------------------------
# Timeframe mapping (GB-BRAIN string → alpaca-py TimeFrame)
# ---------------------------------------------------------------------------
_TF_MAP: dict[str, TimeFrame] = {
    "1Min":  TimeFrame(1,  TimeFrameUnit.Minute),
    "5Min":  TimeFrame(5,  TimeFrameUnit.Minute),
    "15Min": TimeFrame(15, TimeFrameUnit.Minute),
    "1H":    TimeFrame(1,  TimeFrameUnit.Hour),
    "1Hour": TimeFrame(1,  TimeFrameUnit.Hour),
    "1D":    TimeFrame(1,  TimeFrameUnit.Day),
    "1Day":  TimeFrame(1,  TimeFrameUnit.Day),
}

# ---------------------------------------------------------------------------
# Detect paper vs live from ALPACA_BASE_URL
# ---------------------------------------------------------------------------
def _is_paper() -> bool:
    url = getattr(settings, "ALPACA_BASE_URL", "").lower()
    return "paper" in url


# ---------------------------------------------------------------------------
# Client factories
# ---------------------------------------------------------------------------
def _trading_client() -> TradingClient:
    return TradingClient(
        api_key=settings.ALPACA_KEY,
        secret_key=settings.ALPACA_SECRET,
        paper=_is_paper(),
    )


def _data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(
        api_key=settings.ALPACA_KEY,
        secret_key=settings.ALPACA_SECRET,
    )


def _resolve_symbol(symbol: str) -> str:
    resolved = SYMBOL_MAP.get(symbol.upper(), symbol.upper())
    if resolved != symbol.upper():
        logger.debug("Symbol mapped: %s → %s", symbol, resolved)
    return resolved


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def place_order(
    symbol: str,
    qty: float,
    side: str,
    tag: str = "GB-BRAIN",
) -> Optional[dict]:
    """
    Place a market order via the Alpaca REST API.

    Parameters
    ----------
    symbol : str   GB-BRAIN internal symbol (e.g. "SPY", "NAS100").
    qty    : float Number of shares (fractional supported on Alpaca).
    side   : str   "buy" or "sell".
    tag    : str   Client order ID tag prefix. Default "GB-BRAIN".

    Returns
    -------
    dict or None — Order response dict on success, None on failure.
    """
    alpaca_symbol = _resolve_symbol(symbol)
    side_lower = side.lower()
    if side_lower not in ("buy", "sell"):
        logger.error("Invalid side '%s' for %s — must be 'buy' or 'sell'.", side, symbol)
        return None

    order_side = OrderSide.BUY if side_lower == "buy" else OrderSide.SELL
    client_order_id = f"{tag}-{alpaca_symbol}-{side_lower}-{int(time.time())}"

    try:
        client = _trading_client()
        req = MarketOrderRequest(
            symbol=alpaca_symbol,
            qty=qty,
            side=order_side,
            time_in_force=TimeInForce.DAY,
            client_order_id=client_order_id,
        )
        order = client.submit_order(req)
        result = {
            "id":              str(order.id),
            "client_order_id": str(order.client_order_id),
            "symbol":          order.symbol,
            "qty":             str(order.qty),
            "side":            order.side.value,
            "type":            order.order_type.value,
            "status":          order.status.value,
            "submitted_at":    str(order.submitted_at),
        }
        logger.info(
            "Order placed | %s %s × %s | id=%s | tag=%s",
            side_lower.upper(), alpaca_symbol, qty, order.id, tag,
        )
        return result
    except Exception as exc:  # noqa: BLE001
        logger.error("Alpaca error placing order %s %s: %s", side, alpaca_symbol, exc)
        return None


def get_account_balance() -> Optional[float]:
    """
    Retrieve the current portfolio equity from Alpaca.

    Returns
    -------
    float or None — Account equity in USD, or None on failure.
    """
    try:
        client = _trading_client()
        account = client.get_account()
        equity = float(account.equity)
        logger.debug("Account equity: $%.2f", equity)
        return equity
    except Exception as exc:  # noqa: BLE001
        logger.error("Alpaca error fetching account balance: %s", exc)
        return None


def get_positions() -> Optional[list[dict]]:
    """
    Retrieve all open positions from Alpaca.

    Returns
    -------
    list[dict] or None
    """
    try:
        client = _trading_client()
        raw_positions = client.get_all_positions()
        positions = []
        for pos in raw_positions:
            positions.append({
                "symbol":         pos.symbol,
                "qty":            float(pos.qty),
                "avg_price":      float(pos.avg_entry_price),
                "current_price":  float(pos.current_price),
                "unrealized_pnl": float(pos.unrealized_pl),
            })
        logger.debug("Fetched %d open positions.", len(positions))
        return positions
    except Exception as exc:  # noqa: BLE001
        logger.error("Alpaca error fetching positions: %s", exc)
        return None


def close_position(symbol: str) -> Optional[dict]:
    """
    Close an entire open position for the given symbol.

    Returns
    -------
    dict or None
    """
    alpaca_symbol = _resolve_symbol(symbol)
    try:
        client = _trading_client()
        order = client.close_position(alpaca_symbol)
        result = {
            "id":           str(order.id),
            "symbol":       order.symbol,
            "qty":          str(order.qty),
            "side":         order.side.value,
            "type":         order.order_type.value,
            "status":       order.status.value,
            "submitted_at": str(order.submitted_at),
        }
        logger.info("Position closed: %s | order_id=%s", alpaca_symbol, order.id)
        return result
    except Exception as exc:  # noqa: BLE001
        str_exc = str(exc).lower()
        if "position does not exist" in str_exc or "404" in str_exc:
            logger.warning("No open position to close for %s.", alpaca_symbol)
        else:
            logger.error("Alpaca error closing position %s: %s", alpaca_symbol, exc)
        return None


def get_latest_bar(
    symbol: str,
    timeframe: str = "5Min",
) -> Optional[dict]:
    """
    Fetch the most recent completed OHLCV bar for a symbol.

    Returns
    -------
    dict or None
    """
    from datetime import datetime, timedelta, timezone

    alpaca_symbol = _resolve_symbol(symbol)
    alpaca_tf = _TF_MAP.get(timeframe, TimeFrame(5, TimeFrameUnit.Minute))

    try:
        client = _data_client()
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=5)  # wide window to ensure we get bars

        req = StockBarsRequest(
            symbol_or_symbols=alpaca_symbol,
            timeframe=alpaca_tf,
            start=start,
            end=end,
            limit=2,
            adjustment="raw",
        )
        bars_response = client.get_stock_bars(req)
        bars = bars_response.df

        if bars is None or bars.empty:
            logger.warning("No bar data for %s [%s].", alpaca_symbol, timeframe)
            return None

        # Use second-to-last bar — guaranteed closed
        bar = bars.iloc[-2] if len(bars) >= 2 else bars.iloc[-1]
        result = {
            "symbol": alpaca_symbol,
            "time":   str(bar.name),
            "open":   float(bar["open"]),
            "high":   float(bar["high"]),
            "low":    float(bar["low"]),
            "close":  float(bar["close"]),
            "volume": int(bar["volume"]),
        }
        logger.debug(
            "Latest bar %s [%s]: O=%.4f H=%.4f L=%.4f C=%.4f V=%d",
            alpaca_symbol, timeframe,
            result["open"], result["high"], result["low"], result["close"], result["volume"],
        )
        return result
    except Exception as exc:  # noqa: BLE001
        logger.error("Alpaca error fetching bar %s [%s]: %s", alpaca_symbol, timeframe, exc)
        return None
