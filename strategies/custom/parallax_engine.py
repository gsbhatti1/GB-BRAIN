"""
GB-BRAIN — Parallax Engine (Python Port)
==========================================
ORB trap detection across NY/London/Asia sessions.
Ported from GB-PARALLAX v1.6 PineScript.

Usage:
    from strategies.custom.parallax_engine import ParallaxEngine
    engine = ParallaxEngine(preset["parallax"])
    signals = engine.run(df)  # df = OHLCV with datetime index
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import time as dtime


@dataclass
class ParallaxSignal:
    bar: int
    timestamp: object
    direction: int       # 1 = long, -1 = short
    entry_price: float
    stop_loss: float
    tp1: float
    tp2: float
    tp3: float
    score: float         # 0-100
    session: str         # "NY", "LON", "ASIA"
    signal_type: str     # "BREAK_CONFIRM", "TRAP_REVERSAL"
    orb_high: float
    orb_low: float
    orb_range: float
    rsi_value: float
    confirm_count: int
    reason: str


@dataclass
class SessionState:
    name: str
    orh: float = np.nan
    orl: float = np.nan
    orm: float = np.nan
    or_complete: bool = False
    break_detected: bool = False
    break_dir: int = 0
    break_bar: int = -1
    break_price: float = np.nan
    candles_since: int = 0
    consec_conf: int = 0
    trap_detected: bool = False
    trap_bar: int = -1
    flip_detected: bool = False
    flip_dir: int = 0
    flip_confirm: int = 0
    flip_bar: int = -1
    entry_ready: bool = False
    entry_dir: int = 0
    entry_fired: bool = False
    swing_sl: float = np.nan

    def reset_engine(self):
        self.break_detected = False
        self.break_dir = 0
        self.break_bar = -1
        self.break_price = np.nan
        self.candles_since = 0
        self.consec_conf = 0
        self.trap_detected = False
        self.trap_bar = -1
        self.flip_detected = False
        self.flip_dir = 0
        self.flip_confirm = 0
        self.flip_bar = -1
        self.entry_ready = False
        self.entry_dir = 0
        self.entry_fired = False
        self.swing_sl = np.nan

    def reset_orb(self):
        self.orh = np.nan
        self.orl = np.nan
        self.orm = np.nan
        self.or_complete = False
        self.reset_engine()


class ParallaxEngine:
    """GB-PARALLAX v1.6 ORB trap detection — Python implementation."""

    def __init__(self, params: dict):
        self.p = params
        self.orb_minutes = params.get("orb_window_minutes", 5)
        self.confirm_bars = params.get("confirm_candles", 2)
        self.min_target = params.get("min_target_pts", 50)
        self.sl_bars = params.get("swing_sl_bars", 6)
        self.rsi_lo = params.get("rsi_safe_lo", 20)
        self.rsi_hi = params.get("rsi_safe_hi", 80)
        self.max_or = params.get("max_or_range", 120)
        self.min_or = params.get("min_or_range", 5)
        self.trail_pct = params.get("trail_pct", 0.40)
        self.be_1r = params.get("breakeven_at_1r", True)

        self.use_ny = params.get("session_ny", True)
        self.use_lon = params.get("session_london", False)
        self.use_asia = params.get("session_asia", False)

        # Session time windows (ET) — hour:minute
        self.ny_orb_start = dtime(9, 25)
        self.ny_orb_end = dtime(9, 30)
        self.ny_trade_start = dtime(9, 30)
        self.ny_trade_end = dtime(16, 0)

        self.lon_orb_start = dtime(3, 0)
        self.lon_orb_end = dtime(3, 15)
        self.lon_trade_start = dtime(3, 15)
        self.lon_trade_end = dtime(9, 25)

        self.asia_orb_start = dtime(20, 0)
        self.asia_orb_end = dtime(20, 15)
        self.asia_trade_start = dtime(20, 15)
        self.asia_trade_end = dtime(3, 0)

    def _compute_rsi(self, closes: np.ndarray, period: int = 14) -> np.ndarray:
        """Simple RSI calculation."""
        n = len(closes)
        rsi = np.full(n, 50.0)
        if n < period + 1:
            return rsi

        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            if avg_loss == 0:
                rsi[i + 1] = 100
            else:
                rs = avg_gain / avg_loss
                rsi[i + 1] = 100 - (100 / (1 + rs))

        return rsi

    def _in_time_window(self, ts, start: dtime, end: dtime) -> bool:
        """Check if timestamp is within a time window."""
        t = ts.time() if hasattr(ts, 'time') else ts
        if start <= end:
            return start <= t < end
        else:  # Crosses midnight (e.g., Asia 20:00-03:00)
            return t >= start or t < end

    def _run_session_engine(self, sess: SessionState, bar_idx: int,
                            o: float, h: float, l_val: float, c: float,
                            rsi_safe: bool, all_lows: np.ndarray,
                            all_highs: np.ndarray) -> Optional[dict]:
        """Run the core Parallax detection engine for one session on one bar."""
        if not sess.or_complete or sess.entry_fired:
            return None

        orw = abs(sess.orh - sess.orl)
        range_ok = (self.max_or == 0 or orw <= self.max_or) and (self.min_or == 0 or orw >= self.min_or)
        if not range_ok:
            return None

        is_bull = c > o
        is_bear = c < o

        # ─── BREAK DETECTION ───
        if not sess.break_detected:
            if c > sess.orh:
                sess.break_detected = True
                sess.break_dir = 1
                sess.break_bar = bar_idx
                sess.break_price = c
                if is_bull:
                    sess.consec_conf = 1
            elif c < sess.orl:
                sess.break_detected = True
                sess.break_dir = -1
                sess.break_bar = bar_idx
                sess.break_price = c
                if is_bear:
                    sess.consec_conf = 1

            # Check immediate confirm
            if sess.break_detected and not sess.entry_ready:
                if sess.consec_conf >= self.confirm_bars and rsi_safe:
                    sess.entry_ready = True
                    sess.entry_dir = sess.break_dir
            return None

        # ─── POST-BREAK: CONFIRM or TRAP ───
        if bar_idx <= sess.break_bar:
            return None

        sess.candles_since += 1

        # Cumulative body tracking
        if not sess.trap_detected:
            if sess.break_dir == 1 and is_bull:
                sess.consec_conf += 1
            if sess.break_dir == -1 and is_bear:
                sess.consec_conf += 1

        # ─── TRAP: price crosses to opposite side ───
        if not sess.trap_detected:
            if sess.break_dir == -1 and c > sess.orh:
                sess.trap_detected = True
                sess.trap_bar = bar_idx
                sess.flip_detected = True
                sess.flip_dir = 1
                sess.flip_confirm = 0
                sess.flip_bar = bar_idx
                sess.consec_conf = 0
            if sess.break_dir == 1 and c < sess.orl:
                sess.trap_detected = True
                sess.trap_bar = bar_idx
                sess.flip_detected = True
                sess.flip_dir = -1
                sess.flip_confirm = 0
                sess.flip_bar = bar_idx
                sess.consec_conf = 0

        # ─── STANDARD CONFIRM (no trap) ───
        if not sess.trap_detected and not sess.entry_ready:
            if sess.consec_conf >= self.confirm_bars and rsi_safe:
                sess.entry_ready = True
                sess.entry_dir = sess.break_dir

        # ─── FLIP CONFIRM (after trap) ───
        if sess.trap_detected and sess.flip_detected and not sess.entry_ready:
            if bar_idx > sess.flip_bar:
                if sess.flip_dir == 1 and is_bull:
                    sess.flip_confirm += 1
                if sess.flip_dir == -1 and is_bear:
                    sess.flip_confirm += 1
                if sess.flip_confirm >= self.confirm_bars and rsi_safe:
                    sess.entry_ready = True
                    sess.entry_dir = sess.flip_dir

        # ─── SWING SL ───
        if sess.break_detected:
            d = sess.entry_dir if sess.entry_ready else (sess.flip_dir if sess.flip_detected else sess.break_dir)
            sl_start = max(0, bar_idx - self.sl_bars + 1)
            if d == 1:
                sess.swing_sl = float(np.min(all_lows[sl_start:bar_idx + 1]))
            else:
                sess.swing_sl = float(np.max(all_highs[sl_start:bar_idx + 1]))

        # ─── EMIT ENTRY ───
        if sess.entry_ready and not sess.entry_fired:
            sess.entry_fired = True
            sig_type = "TRAP_REVERSAL" if sess.trap_detected else "BREAK_CONFIRM"
            conf_count = sess.flip_confirm if sess.trap_detected else sess.consec_conf
            return {
                "direction": sess.entry_dir,
                "signal_type": sig_type,
                "stop_loss": sess.swing_sl,
                "orb_high": sess.orh,
                "orb_low": sess.orl,
                "orb_range": orw,
                "confirm_count": conf_count,
            }

        return None

    def run(self, df: pd.DataFrame) -> List[ParallaxSignal]:
        """
        Run Parallax engine on OHLCV data.

        Args:
            df: DataFrame with columns [open, high, low, close, volume]
                Index MUST be datetime (timezone-aware preferred, ET assumed).
        """
        o = df["open"].values.astype(float)
        h = df["high"].values.astype(float)
        l = df["low"].values.astype(float)
        c = df["close"].values.astype(float)
        n = len(c)

        rsi = self._compute_rsi(c, 14)
        signals: List[ParallaxSignal] = []

        # Session states
        sessions_config = []
        if self.use_ny:
            sessions_config.append(("NY", self.ny_orb_start, self.ny_orb_end,
                                     self.ny_trade_start, self.ny_trade_end))
        if self.use_lon:
            sessions_config.append(("LON", self.lon_orb_start, self.lon_orb_end,
                                     self.lon_trade_start, self.lon_trade_end))
        if self.use_asia:
            sessions_config.append(("ASIA", self.asia_orb_start, self.asia_orb_end,
                                     self.asia_trade_start, self.asia_trade_end))

        # Per-session state, reset daily
        session_states = {name: SessionState(name=name) for name, *_ in sessions_config}

        last_date = None

        for i in range(n):
            ts = df.index[i]
            current_date = ts.date() if hasattr(ts, 'date') else None

            # Daily reset
            if current_date and current_date != last_date:
                for name in session_states:
                    session_states[name].reset_orb()
                last_date = current_date

            rsi_val = rsi[i]
            rsi_safe = self.rsi_lo <= rsi_val <= self.rsi_hi

            for name, orb_start, orb_end, trade_start, trade_end in sessions_config:
                sess = session_states[name]
                in_orb = self._in_time_window(ts, orb_start, orb_end)
                in_trade = self._in_time_window(ts, trade_start, trade_end) and not in_orb

                # ORB building
                if in_orb:
                    if not sess.or_complete:
                        if np.isnan(sess.orh):
                            sess.orh = h[i]
                            sess.orl = l[i]
                        else:
                            sess.orh = max(sess.orh, h[i])
                            sess.orl = min(sess.orl, l[i])

                # ORB finalize (first bar after ORB window)
                if not in_orb and not sess.or_complete and not np.isnan(sess.orh):
                    sess.orm = (sess.orh + sess.orl) / 2
                    sess.or_complete = True

                # Run engine during trade window
                if in_trade and sess.or_complete:
                    result = self._run_session_engine(
                        sess, i, o[i], h[i], l[i], c[i],
                        rsi_safe, l, h
                    )

                    if result:
                        ep = c[i]
                        d = result["direction"]
                        sl = result["stop_loss"]
                        tp1 = ep + self.min_target * d
                        tp2 = ep + self.min_target * 2 * d
                        tp3 = ep + self.min_target * 3 * d

                        # Score
                        score = 0
                        reason_parts = []
                        if result["signal_type"] == "TRAP_REVERSAL":
                            score += 30
                            reason_parts.append("Trap")
                        else:
                            score += 20
                            reason_parts.append("Break")

                        score += min(result["confirm_count"], 4) * 5
                        reason_parts.append(f"Conf{result['confirm_count']}")

                        if rsi_safe:
                            score += 10
                            reason_parts.append("RSI_OK")

                        orw = result["orb_range"]
                        if self.min_or < orw < self.max_or * 0.7:
                            score += 10
                            reason_parts.append("ORB_clean")

                        if abs(ep - sl) > 0 and self.min_target / abs(ep - sl) >= 1.5:
                            score += 10
                            reason_parts.append("RR>1.5")

                        signals.append(ParallaxSignal(
                            bar=i,
                            timestamp=ts,
                            direction=d,
                            entry_price=ep,
                            stop_loss=sl,
                            tp1=tp1, tp2=tp2, tp3=tp3,
                            score=min(score, 100),
                            session=name,
                            signal_type=result["signal_type"],
                            orb_high=result["orb_high"],
                            orb_low=result["orb_low"],
                            orb_range=orw,
                            rsi_value=rsi_val,
                            confirm_count=result["confirm_count"],
                            reason="+".join(reason_parts),
                        ))

        return signals
