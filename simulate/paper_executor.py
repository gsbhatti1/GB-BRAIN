"""
GB-BRAIN — Paper Executor
===========================
Simulates trade execution without a live broker.
Tracks paper positions, P&L, win rate, drawdown.
Writes all trades to SQLite live_trades table with broker="paper".

Can be used standalone or called from replay_mode / live_observer.

Usage:
    from simulate.paper_executor import PaperExecutor
    executor = PaperExecutor(starting_balance=10000)
    executor.submit(signal, symbol="SPX", strategy="cipher")
    executor.print_summary()

Conventions:
    - SQLite is truth — all paper trades written to live_trades with broker="paper"
    - Capital is priority — RiskManager.can_trade() gate enforced before open
    - STOP → Backup → Patch → Run → Verify
    - .env for secrets — DB path loaded from config.settings
"""

from __future__ import annotations

import logging
import sqlite3
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# ROOT — project root is two levels up from this file (simulate/)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logger = logging.getLogger("gb_brain.paper")

# ---------------------------------------------------------------------------
# DB path (try config.settings; fall back to default)
# ---------------------------------------------------------------------------
try:
    from config import settings as _settings  # type: ignore
    _DB_PATH: Path = Path(getattr(_settings, "DB_PATH", ROOT / "db" / "gb_brain.db"))
except Exception:  # noqa: BLE001
    _DB_PATH = ROOT / "db" / "gb_brain.db"

# ---------------------------------------------------------------------------
# live_trades CREATE TABLE SQL
# ---------------------------------------------------------------------------
_CREATE_LIVE_TRADES = """
CREATE TABLE IF NOT EXISTS live_trades (
    id              TEXT    PRIMARY KEY,
    symbol          TEXT    NOT NULL,
    strategy        TEXT,
    timeframe       TEXT,
    broker          TEXT    DEFAULT 'paper',
    direction       INTEGER,
    entry_price     REAL,
    stop_loss       REAL,
    tp1             REAL,
    tp3             REAL,
    exit_price      REAL,
    exit_reason     TEXT,
    pnl_pts         REAL,
    pnl_pct         REAL,
    rr              REAL,
    score           REAL,
    size            REAL,
    entry_bar       INTEGER,
    exit_bar        INTEGER,
    entry_time      TEXT,
    exit_time       TEXT,
    status          TEXT    DEFAULT 'open'
);
"""

# ---------------------------------------------------------------------------
# Position-size cap
# ---------------------------------------------------------------------------
_MAX_EQUITY_PCT_PER_TRADE = 0.10   # never risk more than 10% of equity on one trade


# ---------------------------------------------------------------------------
# PaperTrade dataclass
# ---------------------------------------------------------------------------

@dataclass
class PaperTrade:
    """Represents one simulated (paper) trade.

    Fields
    ------
    id          : Unique trade identifier (UUID4 hex).
    symbol      : Instrument symbol, e.g. "SPX", "BTC".
    strategy    : Engine name: "cipher", "parallax", "combined", "manual".
    timeframe   : Bar timeframe string, e.g. "5m", "15m".
    direction   : +1 = long, -1 = short.
    entry_price : Price at which the paper order was filled.
    sl          : Stop-loss price.
    tp1         : First take-profit target.
    tp3         : Third / final take-profit target.
    entry_bar   : Bar index at entry (from replay_mode / live_observer).
    exit_price  : Price at which the trade was closed.  None if still open.
    exit_bar    : Bar index at exit.  None if still open.
    exit_reason : One of: "sl", "tp1", "tp3", "trail", "force", "end_of_data".
    pnl_pts     : Profit / loss in price points.
    pnl_pct     : Profit / loss as fraction of entry_price.
    rr          : Realised risk-reward (pnl_pts / initial_risk_pts).
    score       : Signal score from the engine (0.0–1.0).
    entry_time  : ISO-8601 timestamp of entry.
    exit_time   : ISO-8601 timestamp of exit.  None if still open.
    status      : "open" or "closed".
    size        : Notional position size (units or contracts), from position sizing.
    """

    id:           str
    symbol:       str
    strategy:     str
    direction:    int                     # +1 long / -1 short
    entry_price:  float
    sl:           float
    tp1:          float
    tp3:          float
    entry_bar:    int
    score:        float                   = 0.0
    timeframe:    str                     = "5m"
    exit_price:   Optional[float]         = None
    exit_bar:     Optional[int]           = None
    exit_reason:  Optional[str]           = None
    pnl_pts:      Optional[float]         = None
    pnl_pct:      Optional[float]         = None
    rr:           Optional[float]         = None
    entry_time:   Optional[str]           = None
    exit_time:    Optional[str]           = None
    status:       str                     = "open"
    size:         float                   = 1.0

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def initial_risk_pts(self) -> float:
        """Distance in points from entry to stop-loss (always positive)."""
        return abs(self.entry_price - self.sl)

    @property
    def is_open(self) -> bool:
        return self.status == "open"

    @property
    def direction_str(self) -> str:
        return "LONG" if self.direction == 1 else "SHORT"

    def __repr__(self) -> str:  # pragma: no cover
        pnl = f"{self.pnl_pts:+.2f}pts" if self.pnl_pts is not None else "open"
        return (
            f"PaperTrade({self.id[:8]}… {self.symbol} {self.direction_str} "
            f"@ {self.entry_price} → {pnl} [{self.status}])"
        )


# ---------------------------------------------------------------------------
# PaperExecutor
# ---------------------------------------------------------------------------

class PaperExecutor:
    """
    Simulates order execution, tracking open/closed paper trades, equity,
    win rate, and drawdown.  Writes closed trades to SQLite.

    Parameters
    ----------
    starting_balance : float
        Initial paper account balance (default 10 000).
    max_open : int
        Maximum concurrent open paper positions (default 3).
    risk_pct : float
        Fraction of current balance to risk per trade (default 0.01 = 1 %).
    db_path : Optional[Path]
        Override the SQLite database path.  Falls back to config.settings.
    """

    def __init__(
        self,
        starting_balance: float = 10_000.0,
        max_open: int = 3,
        risk_pct: float = 0.01,
        db_path: Optional[Path] = None,
    ) -> None:
        self.starting_balance = float(starting_balance)
        self.balance = self.starting_balance
        self.equity = self.starting_balance   # updated after each trade closes
        self.max_open = max_open
        self.risk_pct = risk_pct
        self._db_path: Path = db_path or _DB_PATH

        self._open_trades:   list[PaperTrade] = []
        self._closed_trades: list[PaperTrade] = []

        # Drawdown tracking
        self._peak_equity: float = self.starting_balance
        self._max_drawdown: float = 0.0

        # Bar counter (incremented by tick())
        self._bar_count: int = 0

        # Ensure DB table exists
        self._ensure_table()

        logger.info(
            "PaperExecutor init | balance=%.2f max_open=%d risk_pct=%.1f%%",
            self.starting_balance, self.max_open, self.risk_pct * 100,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(
        self,
        signal: object,
        symbol: str,
        strategy: str,
        timeframe: str = "5m",
    ) -> Optional[PaperTrade]:
        """
        Open a new paper trade from a signal.

        Enforces:
          - Max open position cap
          - RiskManager.can_trade() gate
          - Position sizing (1 % risk; capped at 10 % equity)

        Parameters
        ----------
        signal    : CipherSignal / dict with direction, entry_price, stop_loss,
                    tp1, tp3, score attributes/keys.
        symbol    : Instrument symbol (e.g. "SPX").
        strategy  : Engine name (e.g. "cipher").
        timeframe : Bar timeframe string.

        Returns
        -------
        PaperTrade if opened, None if rejected.
        """
        # ── Unpack signal ──────────────────────────────────────────────
        if isinstance(signal, dict):
            direction    = int(signal.get("direction", 0))
            entry_price  = float(signal.get("entry_price", 0.0))
            stop_loss    = float(signal.get("stop_loss", 0.0))
            tp1          = float(signal.get("tp1", 0.0))
            tp3          = float(signal.get("tp3", 0.0))
            score        = float(signal.get("score", 0.0))
        else:
            direction    = int(getattr(signal, "direction",    0))
            entry_price  = float(getattr(signal, "entry_price", 0.0))
            stop_loss    = float(getattr(signal, "stop_loss",  0.0))
            tp1          = float(getattr(signal, "tp1",        0.0))
            tp3          = float(getattr(signal, "tp3",        0.0))
            score        = float(getattr(signal, "score",      0.0))

        # ── Validate ───────────────────────────────────────────────────
        if direction == 0:
            logger.debug("submit: direction=0, no trade opened.")
            return None

        if entry_price <= 0 or stop_loss <= 0:
            logger.warning("submit: invalid entry/sl prices (%.4f / %.4f).", entry_price, stop_loss)
            return None

        # ── Cap check ─────────────────────────────────────────────────
        if len(self._open_trades) >= self.max_open:
            logger.info(
                "submit: max_open=%d reached — rejecting %s %s.",
                self.max_open, symbol, strategy,
            )
            return None

        # ── RiskManager gate ──────────────────────────────────────────
        if not self._risk_gate(symbol, strategy):
            logger.info("submit: RiskManager rejected %s %s.", symbol, strategy)
            return None

        # ── Position sizing ───────────────────────────────────────────
        risk_pts = abs(entry_price - stop_loss)
        if risk_pts == 0:
            logger.warning("submit: zero risk distance — skipping.")
            return None

        risk_amount = self.balance * self.risk_pct
        size = risk_amount / risk_pts

        # Clamp to 10% equity max
        max_notional = self.balance * _MAX_EQUITY_PCT_PER_TRADE
        if (size * entry_price) > max_notional:
            size = max_notional / entry_price
            logger.debug("submit: size capped at 10%% equity → %.4f units.", size)

        # ── Build trade ───────────────────────────────────────────────
        trade = PaperTrade(
            id=uuid.uuid4().hex,
            symbol=symbol,
            strategy=strategy,
            timeframe=timeframe,
            direction=direction,
            entry_price=entry_price,
            sl=stop_loss,
            tp1=tp1,
            tp3=tp3,
            entry_bar=self._bar_count,
            score=score,
            entry_time=_utcnow(),
            status="open",
            size=round(size, 6),
        )
        self._open_trades.append(trade)

        logger.info(
            "PAPER OPEN  | %s %s %s | entry=%.4f sl=%.4f tp1=%.4f tp3=%.4f "
            "size=%.4f score=%.3f",
            symbol, strategy, trade.direction_str,
            entry_price, stop_loss, tp1, tp3, size, score,
        )
        return trade

    def tick(
        self,
        bar_high: float,
        bar_low: float,
        bar_close: float,
        bar_time: Optional[str] = None,
    ) -> list[PaperTrade]:
        """
        Process one completed bar against all open positions.

        Checks stop-loss and take-profit levels in sequence:
          1. SL hit → close at stop_loss
          2. TP3 hit → close full position at tp3
          3. TP1 hit → close at tp1 (partial; here simplified to full close)

        Parameters
        ----------
        bar_high  : float  Bar high price.
        bar_low   : float  Bar low price.
        bar_close : float  Bar close price.
        bar_time  : str    ISO-8601 timestamp for the bar (optional).

        Returns
        -------
        List of trades that were closed on this bar.
        """
        self._bar_count += 1
        bt = bar_time or _utcnow()
        closed_this_bar: list[PaperTrade] = []

        for trade in list(self._open_trades):
            direction = trade.direction

            sl_hit  = (direction == 1  and bar_low  <= trade.sl) or \
                      (direction == -1 and bar_high >= trade.sl)
            tp3_hit = (direction == 1  and bar_high >= trade.tp3) or \
                      (direction == -1 and bar_low  <= trade.tp3)
            tp1_hit = (direction == 1  and bar_high >= trade.tp1) or \
                      (direction == -1 and bar_low  <= trade.tp1)

            if sl_hit:
                self.close_trade(trade.id, trade.sl, "sl", bt)
                closed_this_bar.append(trade)
            elif tp3_hit:
                self.close_trade(trade.id, trade.tp3, "tp3", bt)
                closed_this_bar.append(trade)
            elif tp1_hit:
                self.close_trade(trade.id, trade.tp1, "tp1", bt)
                closed_this_bar.append(trade)

        return closed_this_bar

    def close_trade(
        self,
        trade_id: str,
        exit_price: float,
        exit_reason: str,
        exit_time: Optional[str] = None,
    ) -> Optional[PaperTrade]:
        """
        Finalise an open paper trade.

        Parameters
        ----------
        trade_id    : str   Trade UUID hex.
        exit_price  : float Price at exit.
        exit_reason : str   Reason: "sl", "tp1", "tp3", "trail", "force", "end_of_data".
        exit_time   : str   ISO-8601 timestamp (defaults to now).

        Returns
        -------
        Closed PaperTrade, or None if trade_id not found.
        """
        trade = next((t for t in self._open_trades if t.id == trade_id), None)
        if trade is None:
            logger.warning("close_trade: id=%s not found in open trades.", trade_id[:8])
            return None

        pnl_pts = (exit_price - trade.entry_price) * trade.direction
        pnl_pct = pnl_pts / trade.entry_price if trade.entry_price else 0.0
        rr = pnl_pts / trade.initial_risk_pts if trade.initial_risk_pts else 0.0

        trade.exit_price  = exit_price
        trade.exit_bar    = self._bar_count
        trade.exit_reason = exit_reason
        trade.exit_time   = exit_time or _utcnow()
        trade.pnl_pts     = round(pnl_pts, 5)
        trade.pnl_pct     = round(pnl_pct, 6)
        trade.rr          = round(rr, 3)
        trade.status      = "closed"

        # Update balance / equity
        pnl_dollar = pnl_pts * trade.size
        self.balance = max(0.0, self.balance + pnl_dollar)
        self.equity  = self.balance

        # Drawdown
        if self.equity > self._peak_equity:
            self._peak_equity = self.equity
        dd = (self._peak_equity - self.equity) / self._peak_equity if self._peak_equity else 0.0
        if dd > self._max_drawdown:
            self._max_drawdown = dd

        self._open_trades.remove(trade)
        self._closed_trades.append(trade)

        icon = "WIN " if pnl_pts > 0 else "LOSS"
        logger.info(
            "PAPER CLOSE [%s] | %s %s | exit=%.4f reason=%s pnl=%.2fpts rr=%.2f bal=%.2f",
            icon, trade.symbol, trade.direction_str,
            exit_price, exit_reason, pnl_pts, rr, self.balance,
        )
        return trade

    def force_close_all(self, bar_close: float, bar_time: Optional[str] = None) -> int:
        """Close all open trades at bar_close price (end_of_data / cleanup)."""
        bt = bar_time or _utcnow()
        n = len(self._open_trades)
        for trade in list(self._open_trades):
            self.close_trade(trade.id, bar_close, "end_of_data", bt)
        return n

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------

    def get_open_trades(self) -> list[PaperTrade]:
        """Return a copy of the current open trades list."""
        return list(self._open_trades)

    def get_closed_trades(self) -> list[PaperTrade]:
        """Return a copy of the closed trades list."""
        return list(self._closed_trades)

    def get_stats(self) -> dict:
        """
        Return a summary statistics dict.

        Keys
        ----
        equity          : float  Current equity.
        win_rate        : float  Win rate 0–100%.
        pnl_total       : float  Total P&L in points.
        pnl_dollar      : float  Total P&L in dollars (balance delta).
        max_drawdown    : float  Max drawdown fraction (0.0–1.0).
        profit_factor   : float  Gross wins / gross losses (0 if no losers).
        trade_count     : int    Total closed trades.
        open_count      : int    Currently open trades.
        avg_rr          : float  Average realised risk-reward.
        """
        closed = self._closed_trades
        n = len(closed)

        if n == 0:
            return {
                "equity":       self.equity,
                "win_rate":     0.0,
                "pnl_total":    0.0,
                "pnl_dollar":   self.balance - self.starting_balance,
                "max_drawdown": self._max_drawdown,
                "profit_factor": 0.0,
                "trade_count":  0,
                "open_count":   len(self._open_trades),
                "avg_rr":       0.0,
            }

        wins   = [t for t in closed if (t.pnl_pts or 0) > 0]
        losses = [t for t in closed if (t.pnl_pts or 0) <= 0]

        gross_win  = sum((t.pnl_pts or 0) * t.size for t in wins)
        gross_loss = abs(sum((t.pnl_pts or 0) * t.size for t in losses))
        pf = gross_win / gross_loss if gross_loss > 0 else float("inf") if gross_win > 0 else 0.0

        rrs   = [t.rr for t in closed if t.rr is not None]
        avg_rr = sum(rrs) / len(rrs) if rrs else 0.0

        return {
            "equity":       round(self.equity,   2),
            "win_rate":     round(len(wins) / n * 100, 1),
            "pnl_total":    round(sum(t.pnl_pts or 0 for t in closed), 4),
            "pnl_dollar":   round(self.balance - self.starting_balance, 2),
            "max_drawdown": round(self._max_drawdown, 4),
            "profit_factor": round(pf, 3),
            "trade_count":  n,
            "open_count":   len(self._open_trades),
            "avg_rr":       round(avg_rr, 3),
        }

    def print_summary(self) -> None:
        """Print a formatted table of all trades plus summary stats."""
        closed = self._closed_trades

        print("\n" + "=" * 90)
        print(f"  GB-BRAIN Paper Executor — Trade Summary  (balance: {self.balance:,.2f})")
        print("=" * 90)

        if not closed:
            print("  No closed trades yet.")
        else:
            header = (
                f"  {'ID':8s}  {'Symbol':8s}  {'Strat':10s}  {'Dir':5s}  "
                f"{'Entry':>10s}  {'Exit':>10s}  {'PnL pts':>9s}  {'RR':>6s}  {'Reason':12s}"
            )
            print(header)
            print("  " + "-" * 87)
            for t in closed:
                icon = "+" if (t.pnl_pts or 0) > 0 else "-"
                print(
                    f"  {t.id[:8]}  {t.symbol:8s}  {t.strategy:10s}  "
                    f"{t.direction_str:5s}  "
                    f"{t.entry_price:>10.4f}  {(t.exit_price or 0):>10.4f}  "
                    f"{icon}{abs(t.pnl_pts or 0):>8.2f}  {(t.rr or 0):>6.2f}  "
                    f"{(t.exit_reason or ''):12s}"
                )

        stats = self.get_stats()
        print("\n  ── Stats ──────────────────────────────────────────────────")
        print(f"  Trades      : {stats['trade_count']}  (open: {stats['open_count']})")
        print(f"  Win Rate    : {stats['win_rate']:.1f}%")
        print(f"  PnL (pts)   : {stats['pnl_total']:+.4f}")
        print(f"  PnL ($)     : {stats['pnl_dollar']:+,.2f}")
        print(f"  Profit Factor: {stats['profit_factor']:.3f}")
        print(f"  Avg R:R     : {stats['avg_rr']:.3f}")
        print(f"  Max Drawdown: {stats['max_drawdown'] * 100:.2f}%")
        print(f"  Equity      : {stats['equity']:,.2f}")
        print("=" * 90 + "\n")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_to_db(self, trades: Optional[list[PaperTrade]] = None) -> int:
        """
        Write closed paper trades to SQLite live_trades table.

        Parameters
        ----------
        trades : list[PaperTrade], optional
            If None, saves all currently-closed trades.  Performs UPSERT
            (INSERT OR REPLACE) so repeated calls are safe.

        Returns
        -------
        Number of rows written.
        """
        to_save = trades if trades is not None else self._closed_trades
        if not to_save:
            logger.debug("save_to_db: nothing to save.")
            return 0

        sql = """
            INSERT OR REPLACE INTO live_trades
                (id, symbol, strategy, timeframe, broker, direction,
                 entry_price, stop_loss, tp1, tp3,
                 exit_price, exit_reason, pnl_pts, pnl_pct, rr, score,
                 size, entry_bar, exit_bar, entry_time, exit_time, status)
            VALUES
                (?, ?, ?, ?, 'paper', ?,
                 ?, ?, ?, ?,
                 ?, ?, ?, ?, ?, ?,
                 ?, ?, ?, ?, ?, ?)
        """
        rows: list[tuple] = []
        for t in to_save:
            rows.append((
                t.id, t.symbol, t.strategy, t.timeframe, t.direction,
                t.entry_price, t.sl, t.tp1, t.tp3,
                t.exit_price, t.exit_reason,
                t.pnl_pts, t.pnl_pct, t.rr, t.score,
                t.size, t.entry_bar, t.exit_bar,
                t.entry_time, t.exit_time, t.status,
            ))

        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self._db_path) as conn:
                conn.executemany(sql, rows)
                conn.commit()
            logger.info("save_to_db: wrote %d paper trade(s) to %s.", len(rows), self._db_path)
            return len(rows)
        except sqlite3.Error as exc:
            logger.error("save_to_db: SQLite error — %s", exc)
            return 0

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear all trade state and reset balance to starting_balance."""
        self._open_trades   = []
        self._closed_trades = []
        self.balance        = self.starting_balance
        self.equity         = self.starting_balance
        self._peak_equity   = self.starting_balance
        self._max_drawdown  = 0.0
        self._bar_count     = 0
        logger.info("PaperExecutor reset.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _risk_gate(self, symbol: str, strategy: str) -> bool:
        """
        Call RiskManager.can_trade() if available, else allow.
        Returns True if the trade is permitted.
        """
        try:
            from monitor.risk_manager import RiskManager  # type: ignore
            rm = RiskManager()
            allowed = rm.can_trade(symbol=symbol, strategy=strategy)
            if not allowed:
                logger.info(
                    "_risk_gate: RiskManager blocked %s / %s.", symbol, strategy
                )
            return allowed
        except ImportError:
            logger.debug("_risk_gate: RiskManager not importable — allowing by default.")
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning("_risk_gate: RiskManager error (%s) — allowing by default.", exc)
            return True

    def _ensure_table(self) -> None:
        """Create live_trades table if it does not yet exist."""
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(_CREATE_LIVE_TRADES)
                conn.commit()
            logger.debug("live_trades table ensured at %s.", self._db_path)
        except sqlite3.Error as exc:
            logger.error("_ensure_table: SQLite error — %s", exc)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _utcnow() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(tz=timezone.utc).isoformat()
