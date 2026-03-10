"""
GB-BRAIN — Combined Engine (Third Strategy)
=============================================
Fuses Cipher (structure) + Parallax (session traps) + institutional indicators.
Computes a confluence score 0-100 for each potential entry.

This is the engine that aims for 85%+ win rate by only taking
the highest-confluence setups where MULTIPLE independent edges agree.

Institutional features included:
  - Volume Profile / VPOC (calculated from OHLCV)
  - Bollinger Band squeeze detection
  - RSI divergence
  - Cumulative volume delta (estimated from candles)
  - Displacement candle detection
  - Round number proximity
  - Day-of-week filter
  - Kill zone timing
  - News window blocking

Usage:
    from strategies.custom.combined_engine import CombinedEngine
    engine = CombinedEngine(preset)
    signals = engine.run(df)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import time as dtime

from strategies.custom.cipher_engine import CipherEngine, CipherSignal
from strategies.custom.parallax_engine import ParallaxEngine, ParallaxSignal


@dataclass
class CombinedSignal:
    bar: int
    timestamp: object
    direction: int           # 1 long, -1 short
    entry_price: float
    stop_loss: float
    tp1: float
    tp2: float
    tp3: float
    confluence_score: float  # 0-100 — THE number
    source: str              # "CIPHER", "PARALLAX", "BOTH"
    cipher_signal: Optional[CipherSignal]
    parallax_signal: Optional[ParallaxSignal]

    # Institutional context
    bb_squeeze: bool
    rsi_divergence: bool
    displacement: bool
    volume_confirm: bool
    near_vpoc: bool
    near_round_level: bool
    kill_zone_active: bool
    news_blocked: bool
    day_of_week: str

    reason: str              # Human-readable breakdown


class InstitutionalLayer:
    """Computes institutional indicators from OHLCV data."""

    @staticmethod
    def bollinger_bands(close: np.ndarray, period: int = 20, std_mult: float = 2.0):
        """Returns upper, middle, lower bands."""
        n = len(close)
        upper = np.full(n, np.nan)
        middle = np.full(n, np.nan)
        lower = np.full(n, np.nan)
        for i in range(period - 1, n):
            window = close[i - period + 1:i + 1]
            m = np.mean(window)
            s = np.std(window, ddof=1)
            middle[i] = m
            upper[i] = m + std_mult * s
            lower[i] = m - std_mult * s
        return upper, middle, lower

    @staticmethod
    def keltner_channels(close: np.ndarray, high: np.ndarray, low: np.ndarray,
                         period: int = 20, atr_mult: float = 1.5):
        """Returns upper, middle, lower Keltner channels."""
        n = len(close)
        # EMA for middle
        middle = np.full(n, np.nan)
        mult = 2.0 / (period + 1)
        middle[0] = close[0]
        for i in range(1, n):
            middle[i] = close[i] * mult + middle[i - 1] * (1 - mult)

        # ATR
        atr = np.full(n, np.nan)
        tr = np.zeros(n)
        tr[0] = high[0] - low[0]
        for i in range(1, n):
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
        for i in range(period - 1, n):
            atr[i] = np.mean(tr[i - period + 1:i + 1])

        upper = middle + atr_mult * atr
        lower = middle - atr_mult * atr
        return upper, middle, lower

    @staticmethod
    def detect_squeeze(bb_upper, bb_lower, kc_upper, kc_lower) -> np.ndarray:
        """BB inside KC = squeeze. Returns boolean array."""
        return (bb_lower > kc_lower) & (bb_upper < kc_upper)

    @staticmethod
    def rsi(close: np.ndarray, period: int = 14) -> np.ndarray:
        n = len(close)
        rsi = np.full(n, 50.0)
        if n < period + 1:
            return rsi
        deltas = np.diff(close)
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
                rsi[i + 1] = 100 - (100 / (1 + avg_gain / avg_loss))
        return rsi

    @staticmethod
    def rsi_divergence(close: np.ndarray, rsi: np.ndarray, lookback: int = 20) -> np.ndarray:
        """Detect RSI divergence. Returns array: 1=bullish div, -1=bearish div, 0=none."""
        n = len(close)
        div = np.zeros(n, dtype=int)
        for i in range(lookback, n):
            window_c = close[i - lookback:i + 1]
            window_r = rsi[i - lookback:i + 1]
            # Bearish: price making HH, RSI making LH
            if close[i] > np.max(window_c[:-1]) and rsi[i] < np.max(window_r[:-1]):
                div[i] = -1
            # Bullish: price making LL, RSI making HL
            if close[i] < np.min(window_c[:-1]) and rsi[i] > np.min(window_r[:-1]):
                div[i] = 1
        return div

    @staticmethod
    def volume_delta(open_arr: np.ndarray, close: np.ndarray,
                     high: np.ndarray, low: np.ndarray, volume: np.ndarray) -> np.ndarray:
        """Estimate buying vs selling pressure from candle structure."""
        n = len(close)
        delta = np.zeros(n)
        for i in range(n):
            rng = high[i] - low[i]
            if rng > 0:
                buy_pct = (close[i] - low[i]) / rng
                sell_pct = (high[i] - close[i]) / rng
                delta[i] = volume[i] * (buy_pct - sell_pct)
        return delta

    @staticmethod
    def detect_displacement(open_arr: np.ndarray, close: np.ndarray,
                            high: np.ndarray, low: np.ndarray,
                            atr: np.ndarray, threshold: float = 1.5) -> np.ndarray:
        """Displacement = strong candle body > threshold * ATR."""
        body = np.abs(close - open_arr)
        is_disp = np.zeros(len(close), dtype=bool)
        for i in range(len(close)):
            if not np.isnan(atr[i]) and atr[i] > 0:
                is_disp[i] = body[i] > threshold * atr[i]
        return is_disp

    @staticmethod
    def compute_vpoc(high: np.ndarray, low: np.ndarray, volume: np.ndarray,
                     close: np.ndarray, lookback: int = 50, bins: int = 30) -> np.ndarray:
        """Compute rolling VPOC (Volume Point of Control)."""
        n = len(close)
        vpoc = np.full(n, np.nan)
        for i in range(lookback, n):
            h_window = high[i - lookback:i + 1]
            l_window = low[i - lookback:i + 1]
            v_window = volume[i - lookback:i + 1]

            price_min = np.min(l_window)
            price_max = np.max(h_window)
            if price_max <= price_min:
                continue

            bin_edges = np.linspace(price_min, price_max, bins + 1)
            vol_profile = np.zeros(bins)

            for j in range(len(h_window)):
                for b in range(bins):
                    if l_window[j] <= bin_edges[b + 1] and h_window[j] >= bin_edges[b]:
                        vol_profile[b] += v_window[j] / max(1, np.sum(
                            (l_window[j] <= bin_edges[1:]) & (h_window[j] >= bin_edges[:-1])
                        ))

            poc_bin = np.argmax(vol_profile)
            vpoc[i] = (bin_edges[poc_bin] + bin_edges[poc_bin + 1]) / 2

        return vpoc

    @staticmethod
    def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
        n = len(close)
        tr = np.zeros(n)
        atr = np.full(n, np.nan)
        tr[0] = high[0] - low[0]
        for i in range(1, n):
            tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
        for i in range(period - 1, n):
            atr[i] = np.mean(tr[i - period + 1:i + 1])
        return atr


class CombinedEngine:
    """
    The THIRD strategy: Cipher + Parallax + Institutional features.
    Only fires when confluence score exceeds ticker-specific threshold.
    """

    def __init__(self, preset: dict):
        self.preset = preset
        self.cipher = CipherEngine(preset.get("cipher", {}))
        self.parallax = ParallaxEngine(preset.get("parallax", {}))
        self.combined_cfg = preset.get("combined", {})
        self.threshold = self.combined_cfg.get("entry_threshold", 65)
        self.weights = self.combined_cfg.get("weights", {})
        self.round_increment = preset.get("round_increment", 250)
        self.kill_zones = preset.get("kill_zones", [])
        self.news_windows = preset.get("news_windows", [])
        self.inst = InstitutionalLayer()

    def _is_in_kill_zone(self, ts) -> Tuple:
        """Check if timestamp is in a kill zone. Returns (bool, weight)."""
        if not hasattr(ts, 'time'):
            return False, 0
        t = ts.time()
        for kz in self.kill_zones:
            start = dtime(*[int(x) for x in kz["start"].split(":")])
            end = dtime(*[int(x) for x in kz["end"].split(":")])
            if start <= t < end:
                return True, kz.get("weight", 1.0)
        return False, 0

    def _is_news_blocked(self, ts) -> bool:
        if not hasattr(ts, 'time'):
            return False
        t = ts.time()
        for nw in self.news_windows:
            start = dtime(*[int(x) for x in nw["start"].split(":")])
            end = dtime(*[int(x) for x in nw["end"].split(":")])
            if start <= t < end:
                return True
        return False

    def run(self, df: pd.DataFrame) -> List[CombinedSignal]:
        """
        Run combined engine. Produces signals ONLY when confluence is high enough.

        Args:
            df: OHLCV DataFrame with datetime index
        """
        o = df["open"].values.astype(float)
        h = df["high"].values.astype(float)
        l = df["low"].values.astype(float)
        c = df["close"].values.astype(float)
        v = df["volume"].values.astype(float) if "volume" in df.columns else np.ones(len(df))
        n = len(c)

        # ─── Run sub-engines ───
        cipher_signals = self.cipher.run(df)
        parallax_signals = self.parallax.run(df)

        # Index signals by bar for fast lookup
        cipher_by_bar = {s.bar: s for s in cipher_signals}
        parallax_by_bar = {s.bar: s for s in parallax_signals}

        # ─── Compute institutional indicators ───
        atr = self.inst.atr(h, l, c, 14)
        rsi_arr = self.inst.rsi(c, 14)
        rsi_div = self.inst.rsi_divergence(c, rsi_arr, 20)
        bb_u, bb_m, bb_l = self.inst.bollinger_bands(c, 20, 2.0)
        kc_u, kc_m, kc_l = self.inst.keltner_channels(c, h, l, 20, 1.5)
        squeeze = self.inst.detect_squeeze(bb_u, bb_l, kc_u, kc_l)
        delta = self.inst.volume_delta(o, c, h, l, v)
        displacement = self.inst.detect_displacement(o, c, h, l, atr, 1.5)
        vpoc = self.inst.compute_vpoc(h, l, v, c, lookback=50, bins=30)

        # Cumulative delta (rolling 10-bar sum)
        cum_delta = np.convolve(delta, np.ones(10), mode='same')

        # ─── Score signals using proximity window (not exact bar match) ───
        combined_signals: List[CombinedSignal] = []
        WINDOW = 5  # Look for matching signals within 5 bars

        # Build lookup: for each bar, find nearest cipher/parallax signal within window
        def find_nearby(signals_dict, bar, window=WINDOW):
            for offset in range(window + 1):
                if bar - offset in signals_dict:
                    return signals_dict[bar - offset]
                if bar + offset in signals_dict:
                    return signals_dict[bar + offset]
            return None

        # Score every bar that has at least one signal
        all_signal_bars = set(cipher_by_bar.keys()) | set(parallax_by_bar.keys())

        for bar in sorted(all_signal_bars):
            if bar >= n:
                continue

            ts = df.index[bar]
            ci = cipher_by_bar.get(bar) or find_nearby(cipher_by_bar, bar)
            px = parallax_by_bar.get(bar) or find_nearby(parallax_by_bar, bar)

            # Determine direction (both must agree if both present)
            if ci and px:
                if ci.direction != px.direction:
                    continue  # Conflicting signals — skip
                direction = ci.direction
                source = "BOTH"
            elif ci:
                direction = ci.direction
                source = "CIPHER"
            elif px:
                direction = px.direction
                source = "PARALLAX"
            else:
                continue

            # News block
            news_blocked = self._is_news_blocked(ts)
            if news_blocked:
                continue

            # ─── CONFLUENCE SCORING ───
            score = 0
            reasons = []
            w = self.weights

            # Source signals
            if ci:
                score += w.get("choch_active", 20) if ci.choch_active else w.get("choch_active", 20) * 0.5
                reasons.append(f"CI({ci.score:.0f})")
                if ci.fvg_quality == "G":
                    score += w.get("fvg_golden", 15)
                    reasons.append("FVG_G")
                if ci.near_ob:
                    score += w.get("ob_proximity", 10)
                    reasons.append("OB")
                if ci.in_ote:
                    score += w.get("ote_zone", 10)
                    reasons.append("OTE")
                if (direction == 1 and ci.zone == "discount") or (direction == -1 and ci.zone == "premium"):
                    score += w.get("premium_discount", 5)
                    reasons.append("Zone")

            if px:
                if px.signal_type == "TRAP_REVERSAL":
                    score += w.get("parallax_trap", 20)
                    reasons.append("TRAP")
                else:
                    score += w.get("parallax_trap", 20) * 0.6
                    reasons.append("BRK")
                conf_ratio = px.confirm_count / max(1, self.parallax.confirm_bars)
                score += w.get("parallax_confirm", 10) * min(conf_ratio, 1.0)

            # BOTH engines agree = massive bonus
            if ci and px:
                score += w.get("both_agree_bonus", 25)
                reasons.append("BOTH★")

            # RSI safe zone
            if self.parallax.rsi_lo <= rsi_arr[bar] <= self.parallax.rsi_hi:
                score += w.get("rsi_safe", 5)

            # Bollinger position
            if not np.isnan(bb_l[bar]) and not np.isnan(bb_u[bar]):
                bb_range = bb_u[bar] - bb_l[bar]
                if bb_range > 0:
                    bb_pos = (c[bar] - bb_l[bar]) / bb_range
                    # Good: buying near lower band, selling near upper
                    if direction == 1 and bb_pos < 0.3:
                        score += w.get("bollinger_position", 5)
                        reasons.append("BB_low")
                    elif direction == -1 and bb_pos > 0.7:
                        score += w.get("bollinger_position", 5)
                        reasons.append("BB_high")

            # BB Squeeze (compression = breakout coming)
            bb_squeeze = bool(squeeze[bar]) if bar < len(squeeze) else False
            if bb_squeeze:
                score += 5
                reasons.append("Squeeze")

            # RSI divergence
            rsi_div_val = bool(rsi_div[bar] == direction) if bar < len(rsi_div) else False
            if rsi_div_val:
                score += 8
                reasons.append("RSI_div")

            # Volume confirmation
            vol_confirm = False
            if bar >= 20:
                avg_vol = np.mean(v[bar - 20:bar])
                if avg_vol > 0 and v[bar] > avg_vol * 1.2:
                    vol_confirm = True
                    score += w.get("volume_above_avg", 5)
                    reasons.append("Vol+")

            # Volume delta agrees with direction
            if (direction == 1 and cum_delta[bar] > 0) or (direction == -1 and cum_delta[bar] < 0):
                score += 3
                reasons.append("Delta")

            # Displacement candle
            disp = bool(displacement[bar]) if bar < len(displacement) else False
            if disp:
                score += 5
                reasons.append("Disp")

            # VPOC proximity
            near_vpoc = False
            if not np.isnan(vpoc[bar]) and not np.isnan(atr[bar]) and atr[bar] > 0:
                if abs(c[bar] - vpoc[bar]) < atr[bar] * 0.5:
                    near_vpoc = True
                    score += 5
                    reasons.append("VPOC")

            # Round level proximity
            near_round = False
            if self.round_increment > 0:
                nearest = round(c[bar] / self.round_increment) * self.round_increment
                if abs(c[bar] - nearest) < self.round_increment * 0.1:
                    near_round = True
                    score += w.get("round_level_proximity", 7)
                    reasons.append(f"R{nearest:.0f}")

            # Kill zone
            kz_active, kz_weight = self._is_in_kill_zone(ts)
            if kz_active:
                score *= (0.8 + 0.2 * kz_weight)  # Scale by kill zone quality

            # Day of week
            dow = ""
            if hasattr(ts, 'strftime'):
                dow = ts.strftime("%A")
                if dow == "Monday":
                    score *= 0.85  # Monday penalty
                elif dow == "Wednesday":
                    score *= 1.05  # Wednesday bonus

            # ─── THRESHOLD CHECK ───
            if score < self.threshold:
                continue

            # ─── Build final signal ───
            ep = c[bar]
            if ci:
                sl = ci.stop_loss
                tp1, tp2, tp3 = ci.tp1, ci.tp2, ci.tp3
            elif px:
                sl = px.stop_loss
                tp1, tp2, tp3 = px.tp1, px.tp2, px.tp3
            else:
                continue

            combined_signals.append(CombinedSignal(
                bar=bar,
                timestamp=ts,
                direction=direction,
                entry_price=ep,
                stop_loss=sl,
                tp1=tp1, tp2=tp2, tp3=tp3,
                confluence_score=round(score, 1),
                source=source,
                cipher_signal=ci,
                parallax_signal=px,
                bb_squeeze=bb_squeeze,
                rsi_divergence=rsi_div_val,
                displacement=disp,
                volume_confirm=vol_confirm,
                near_vpoc=near_vpoc,
                near_round_level=near_round,
                kill_zone_active=kz_active,
                news_blocked=False,
                day_of_week=dow,
                reason=" | ".join(reasons),
            ))

        return combined_signals
