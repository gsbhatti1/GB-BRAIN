"""
alpaca_bridge.py — GB-BRAIN Alpaca Broker Bridge
=================================================
Handles all Alpaca REST API interactions for US stocks and indices.

Pattern mirrors oanda_bridge.py exactly.

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
from typing import Optional

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError

from config import settings

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.alpaca")

# ---------------------------------------------------------------------------
# Symbol mapping
# ---------------------------------------------------------------------------
# GB-BRAIN internal symbol  →  Alpaca tradeable symbol
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
    "SPX":    "SPY",    # No direct SPX ETF — route to SPY
    "NAS100": "QQQ",    # Route to QQQ proxy
    "US30":   "DIA",    # Route to DIA proxy
    "ARKK":   "ARKK",
    "GLD":    "GLD",
    "SLV":    "SLV",
    "TLT":    "TLT",
    "IWM":    "IWM",
}

# ---------------------------------------------------------------------------
# Timeframe mapping (GB-BRAIN string → Alpaca TimeFrame)
# ---------------------------------------------------------------------------
_TF_MAP: dict[str, str] = {
    "1Min":  "1Min",
    "5Min":  "5Min",
    "15Min": "15Min",
    "1H":    "1Hour",
    "1Hour": "1Hour",
    "1D":    "1Day",
    "1Day":  "1Day",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_client() -> tradeapi.REST:
    """
    Instantiate and return an Alpaca REST client using credentials from
    config.settings.  The environment (paper vs live) is determined solely
    by ALPACA_BASE_URL — no logic branch required.

    Returns
    -------
    tradeapi.REST
        Authenticated Alpaca REST client.
    """
    return tradeapi.REST(
        key_id=settings.ALPACA_KEY,
        secret_key=settings.ALPACA_SECRET,
        base_url=settings.ALPACA_BASE_URL,
        api_version="v2",
    )


def _resolve_symbol(symbol: str) -> str:
    """
    Translate a GB-BRAIN internal symbol to an Alpaca-tradeable symbol.

    Parameters
    ----------
    symbol : str
        GB-BRAIN internal symbol (e.g. "NAS100", "SPX").

    Returns
    -------
    str
        Alpaca tradeable symbol (e.g. "QQQ", "SPY").
    """
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
    symbol : str
        GB-BRAIN internal symbol (e.g. "SPY", "NVDA", "NAS100").
    qty : float
        Number of shares (fractional supported on Alpaca).
    side : str
        "buy" or "sell".
    tag : str
        Client order ID tag prefix for traceability. Default "GB-BRAIN".

    Returns
    -------
    dict or None
        Order response dict on success, None on failure.

    Example
    -------
    >>> place_order("SPY", 10, "buy")
    {'id': '...', 'symbol': 'SPY', 'qty': '10', 'side': 'buy', ...}
    """
    alpaca_symbol = _resolve_symbol(symbol)
    side_lower = side.lower()
    if side_lower not in ("buy", "sell"):
        logger.error("Invalid side '%s' for %s — must be 'buy' or 'sell'.", side, symbol)
        return None

    client_order_id = f"{tag}-{alpaca_symbol}-{side_lower}-{int(__import__('time').time())}"

    try:
        api = _get_client()
        order = api.submit_order(
            symbol=alpaca_symbol,
            qty=qty,
            side=side_lower,
            type="market",
            time_in_force="day",
            client_order_id=client_order_id,
        )
        result = {
            "id":              order.id,
            "client_order_id": order.client_order_id,
            "symbol":          order.symbol,
            "qty":             order.qty,
            "side":            order.side,
            "type":            order.type,
            "status":          order.status,
            "submitted_at":    str(order.submitted_at),
        }
        logger.info(
            "Order placed | %s %s × %s | id=%s | tag=%s",
            side_lower.upper(), alpaca_symbol, qty, order.id, tag,
        )
        return result
    except APIError as exc:
        logger.error("Alpaca APIError placing order %s %s: %s", side, alpaca_symbol, exc)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error placing order %s %s: %s", side, alpaca_symbol, exc)
        return None


def get_account_balance() -> Optional[float]:
    """
    Retrieve the current portfolio equity (cash + unrealized P&L) from Alpaca.

    Returns
    -------
    float or None
        Account equity as a float (USD), or None on failure.

    Example
    -------
    >>> get_account_balance()
    24831.57
    """
    try:
        api = _get_client()
        account = api.get_account()
        equity = float(account.equity)
        logger.debug("Account equity: $%.2f", equity)
        return equity
    except APIError as exc:
        logger.error("Alpaca APIError fetching account balance: %s", exc)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error fetching account balance: %s", exc)
        return None


def get_positions() -> Optional[list[dict]]:
    """
    Retrieve all open positions from Alpaca.

    Returns
    -------
    list[dict] or None
        List of position dicts, each containing:
            symbol          (str)   — Alpaca symbol
            qty             (float) — number of shares held
            avg_price       (float) — average entry price
            current_price   (float) — latest market price
            unrealized_pnl  (float) — unrealized P&L in USD
        Returns None on API failure.

    Example
    -------
    >>> get_positions()
    [{'symbol': 'SPY', 'qty': 10.0, 'avg_price': 512.3, ...}]
    """
    try:
        api = _get_client()
        raw_positions = api.list_positions()
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
    except APIError as exc:
        logger.error("Alpaca APIError fetching positions: %s", exc)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error fetching positions: %s", exc)
        return None


def close_position(symbol: str) -> Optional[dict]:
    """
    Close an entire open position for the given symbol.

    Parameters
    ----------
    symbol : str
        GB-BRAIN internal symbol (e.g. "SPY", "NVDA").

    Returns
    -------
    dict or None
        Closing order dict on success, None on failure or if no position exists.

    Example
    -------
    >>> close_position("SPY")
    {'id': '...', 'symbol': 'SPY', 'side': 'sell', 'status': 'pending_new', ...}
    """
    alpaca_symbol = _resolve_symbol(symbol)
    try:
        api = _get_client()
        order = api.close_position(alpaca_symbol)
        result = {
            "id":           order.id,
            "symbol":       order.symbol,
            "qty":          order.qty,
            "side":         order.side,
            "type":         order.type,
            "status":       order.status,
            "submitted_at": str(order.submitted_at),
        }
        logger.info("Position closed: %s | order_id=%s", alpaca_symbol, order.id)
        return result
    except APIError as exc:
        # 422 = no position exists — not a hard error
        if "position does not exist" in str(exc).lower() or "404" in str(exc):
            logger.warning("No open position to close for %s.", alpaca_symbol)
        else:
            logger.error("Alpaca APIError closing position %s: %s", alpaca_symbol, exc)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error closing position %s: %s", alpaca_symbol, exc)
        return None


def get_latest_bar(
    symbol: str,
    timeframe: str = "5Min",
) -> Optional[dict]:
    """
    Fetch the most recent completed OHLCV bar for a symbol.

    Parameters
    ----------
    symbol : str
        GB-BRAIN internal symbol (e.g. "SPY", "NAS100").
    timeframe : str
        Bar timeframe string. Supported: "1Min", "5Min", "15Min",
        "1H", "1Hour", "1D", "1Day". Default "5Min".

    Returns
    -------
    dict or None
        OHLCV bar dict:
            symbol  (str)   — resolved Alpaca symbol
            time    (str)   — bar timestamp (ISO 8601)
            open    (float)
            high    (float)
            low     (float)
            close   (float)
            volume  (int)
        Returns None on failure.

    Example
    -------
    >>> get_latest_bar("SPY", "5Min")
    {'symbol': 'SPY', 'time': '2026-03-28T13:35:00Z', 'open': 513.1, ...}
    """
    alpaca_symbol = _resolve_symbol(symbol)
    alpaca_tf = _TF_MAP.get(timeframe, timeframe)

    try:
        api = _get_client()
        bars = api.get_bars(
            alpaca_symbol,
            alpaca_tf,
            limit=2,          # fetch 2; last bar may be in-progress
            adjustment="raw",
        ).df

        if bars is None or bars.empty:
            logger.warning("No bar data returned for %s [%s].", alpaca_symbol, alpaca_tf)
            return None

        # Use second-to-last bar — guaranteed closed
        bar = bars.iloc[-2] if len(bars) >= 2 else bars.iloc[-1]
        result = {
            "symbol": alpaca_symbol,
            "time":   str(bar.name),  # DatetimeIndex
            "open":   float(bar["open"]),
            "high":   float(bar["high"]),
            "low":    float(bar["low"]),
            "close":  float(bar["close"]),
            "volume": int(bar["volume"]),
        }
        logger.debug(
            "Latest bar %s [%s]: O=%.4f H=%.4f L=%.4f C=%.4f V=%d",
            alpaca_symbol, alpaca_tf,
            result["open"], result["high"], result["low"], result["close"], result["volume"],
        )
        return result
    except APIError as exc:
        logger.error("Alpaca APIError fetching bar %s [%s]: %s", alpaca_symbol, alpaca_tf, exc)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error fetching bar %s [%s]: %s", alpaca_symbol, alpaca_tf, exc)
        return None
