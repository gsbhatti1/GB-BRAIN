"""
GB-BRAIN — Cipher Engine (Python Port)
========================================
Structure decoder: BOS, ChoCh, FVG, OB, OTE, Entry Signals.
Ported from GB-CIPHER v1.2 PineScript with all bug fixes.

Usage:
    from strategies.custom.cipher_engine import CipherEngine
    engine = CipherEngine(preset["cipher"])
    signals = engine.run(df)  # df = OHLCV DataFrame
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


@dataclass
class SwingPoint:
    price: float
    bar: int
    type: str  # "HH", "LH", "HL", "LL"


@dataclass
class FVGZone:
    top: float
    bot: float
    bar: int
    direction: int  # 1 bull, -1 bear
    mitigated: bool = False
    fib_zone: str = "?"  # G, D, E, P


@dataclass
class OBZone:
    top: float
    bot: float
    bar: int
    direction: int
    mitigated: bool = False
    is_breaker: bool = False


@dataclass
class CipherSignal:
    bar: int
    timestamp: object
    direction: int  # 1 = long, -1 = short
    entry_price: float
    stop_loss: float
    tp1: float
    tp2: float
    tp3: float
    score: float  # 0-100 confluence score
    reason: str
    trend: int
    zone: str  # "premium", "discount", "equilibrium"
    fvg_quality: str  # G, D, E, P or ""
    choch_active: bool
    near_ob: bool
    in_ote: bool


class CipherEngine:
    """GB-CIPHER v1.2 structure decoder — Python implementation."""

    def __init__(self, params: dict):
        self.p = params
        self.swing_len = params.get("swing_lookback", 5)
        self.cooldown = params.get("entry_cooldown_bars", 2)
        self.choch_window = params.get("choch_entry_window", 15)
        self.target = params.get("min_target_pts", 50)
        self.sl_bars = params.get("swing_sl_bars", 6)
        self.ote_low = params.get("ote_low", 0.62)
        self.ote_high = params.get("ote_high", 0.79)
        self.trail_pct = params.get("trail_pct", 0.40)
        self.be_at_1r = params.get("breakeven_at_1r", True)

        # Filters
        self.req_choch = params.get("require_choch", True)
        self.req_fvg = params.get("require_fvg", False)
        self.req_ote = params.get("require_ote", False)
        self.req_discount = params.get("require_discount", False)
        self.req_trend = params.get("require_trend_agree", True)
        self.req_swing = params.get("require_swing_valid", True)
        self.req_break = params.get("require_break_swing", True)

    def _detect_pivots(self, highs: np.ndarray, lows: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Detect pivot highs and lows using swing lookback."""
        n = len(highs)
        piv_high = np.full(n, np.nan)
        piv_low = np.full(n, np.nan)
        sl = self.swing_len

        for i in range(sl, n - sl):
            # Pivot high: highest in both directions
            is_ph = True
            for j in range(1, sl + 1):
                if highs[i] <= highs[i - j] or highs[i] <= highs[i + j]:
                    is_ph = False
                    break
            if is_ph:
                piv_high[i + sl] = highs[i]  # Confirmed sl bars later

            # Pivot low: lowest in both directions
            is_pl = True
            for j in range(1, sl + 1):
                if lows[i] >= lows[i - j] or lows[i] >= lows[i + j]:
                    is_pl = False
                    break
            if is_pl:
                piv_low[i + sl] = lows[i]

        return piv_high, piv_low

    def _classify_fvg(self, price: float, sw_high: float, sw_low: float, direction: int) -> str:
        """Classify FVG position in dealing range."""
        if np.isnan(sw_high) or np.isnan(sw_low) or sw_high <= sw_low:
            return "?"
        rng = sw_high - sw_low
        if direction == 1:  # Bullish FVG
            depth = (sw_high - price) / rng
            if 0.618 <= depth <= 0.705:
                return "G"  # Golden pocket
            elif 0.50 <= depth < 0.618:
                return "D"  # Discount
            elif 0.382 <= depth < 0.50:
                return "E"  # Equilibrium
            else:
                return "P"  # Premium
        else:  # Bearish FVG
            depth = (price - sw_low) / rng
            if 0.618 <= depth <= 0.705:
                return "G"
            elif 0.50 <= depth < 0.618:
                return "P"
            elif 0.382 <= depth < 0.50:
                return "E"
            else:
                return "D"

    def run(self, df: pd.DataFrame) -> List[CipherSignal]:
        """
        Run Cipher engine on OHLCV data.

        Args:
            df: DataFrame with columns [open, high, low, close, volume]
                Index should be datetime.

        Returns:
            List of CipherSignal objects
        """
        o = df["open"].values.astype(float)
        h = df["high"].values.astype(float)
        l = df["low"].values.astype(float)
        c = df["close"].values.astype(float)
        v = df["volume"].values.astype(float) if "volume" in df.columns else np.ones(len(df))
        n = len(c)
        sl = self.swing_len

        # Detect pivots
        piv_high, piv_low = self._detect_pivots(h, l)

        # State variables
        trend = 0
        last_sw_h = np.nan
        last_sw_l = np.nan
        last_sw_h_bar = -1
        last_sw_l_bar = -1
        prev_sw_h = np.nan
        prev_sw_l = np.nan
        last_high_type = ""
        last_low_type = ""
        last_struct_bar = 0

        # ChoCh tracking (v1.2 fix)
        choch_bull_break = np.nan
        choch_bear_break = np.nan
        choch_bull_bar = -999
        choch_bear_bar = -999
        choch_bull_active = False
        choch_bear_active = False

        # FVG and OB zones
        fvg_zones: List[FVGZone] = []
        ob_zones: List[OBZone] = []

        # Signals output
        signals: List[CipherSignal] = []
        last_sig_bar = -999
        last_sig_dir = 0
        cooldown_bars = 10  # Signal cooldown

        # Trade state
        active = False
        is_long = False
        entry_price = 0.0
        sl_level = 0.0

        for i in range(max(sl * 2 + 2, 3), n):
            bos_now = False
            bos_dir = 0
            choch_now = False
            choch_dir = 0

            # ─── SWING HIGH ───
            if not np.isnan(piv_high[i]):
                prev_sw_h = last_sw_h
                last_sw_h_bar = i - sl
                last_sw_h = piv_high[i]
                if not np.isnan(prev_sw_h):
                    if piv_high[i] > prev_sw_h:
                        last_high_type = "HH"
                        if trend == 1:
                            bos_now, bos_dir = True, 1
                        elif trend == -1:
                            choch_now, choch_dir = True, 1
                            trend = 1
                            choch_bull_break = prev_sw_h
                            choch_bull_bar = i
                            choch_bull_active = True
                        else:
                            trend = 1
                            bos_now, bos_dir = True, 1
                        last_struct_bar = i
                    else:
                        last_high_type = "LH"

            # ─── SWING LOW ───
            if not np.isnan(piv_low[i]):
                prev_sw_l = last_sw_l
                last_sw_l_bar = i - sl
                last_sw_l = piv_low[i]
                if not np.isnan(prev_sw_l):
                    if piv_low[i] < prev_sw_l:
                        last_low_type = "LL"
                        if trend == -1:
                            bos_now, bos_dir = True, -1
                        elif trend == 1:
                            choch_now, choch_dir = True, -1
                            trend = -1
                            choch_bear_break = prev_sw_l
                            choch_bear_bar = i
                            choch_bear_active = True
                        else:
                            trend = -1
                            bos_now, bos_dir = True, -1
                        last_struct_bar = i
                    else:
                        last_low_type = "HL"

            # Expire ChoCh windows
            if choch_bull_active and (i - choch_bull_bar) > self.choch_window:
                choch_bull_active = False
            if choch_bear_active and (i - choch_bear_bar) > self.choch_window:
                choch_bear_active = False

            # ─── FVG DETECTION ───
            if i >= 2:
                # Bullish FVG
                bull_gap_top = l[i]
                bull_gap_bot = h[i - 2]
                if bull_gap_top > bull_gap_bot and c[i - 1] > o[i - 1]:
                    mid = (bull_gap_top + bull_gap_bot) / 2
                    fib = self._classify_fvg(mid, last_sw_h, last_sw_l, 1)
                    fvg_zones.append(FVGZone(bull_gap_top, bull_gap_bot, i - 2, 1, False, fib))

                # Bearish FVG
                bear_gap_top = l[i - 2]
                bear_gap_bot = h[i]
                if bear_gap_top > bear_gap_bot and c[i - 1] < o[i - 1]:
                    mid = (bear_gap_top + bear_gap_bot) / 2
                    fib = self._classify_fvg(mid, last_sw_h, last_sw_l, -1)
                    fvg_zones.append(FVGZone(bear_gap_top, bear_gap_bot, i - 2, -1, False, fib))

            # FVG mitigation
            for fvg in fvg_zones:
                if not fvg.mitigated:
                    mid = (fvg.top + fvg.bot) / 2
                    if fvg.direction == 1 and l[i] <= mid:
                        fvg.mitigated = True
                    if fvg.direction == -1 and h[i] >= mid:
                        fvg.mitigated = True

            # ─── ORDER BLOCK DETECTION ───
            if (bos_now or choch_now):
                imp_dir = bos_dir if bos_now else choch_dir
                imp_bar = last_sw_h_bar if imp_dir == 1 else last_sw_l_bar
                if imp_bar >= 0:
                    if imp_dir == 1:
                        for j in range(1, min(11, imp_bar + 1)):
                            idx = imp_bar - j
                            if idx >= 0 and c[idx] < o[idx]:
                                ob_zones.append(OBZone(h[idx], l[idx], idx, 1))
                                break
                    else:
                        for j in range(1, min(11, imp_bar + 1)):
                            idx = imp_bar - j
                            if idx >= 0 and c[idx] > o[idx]:
                                ob_zones.append(OBZone(h[idx], l[idx], idx, -1))
                                break

            # OB mitigation
            for ob in ob_zones:
                if not ob.mitigated:
                    if i - ob.bar > 50:
                        ob.mitigated = True
                    elif ob.direction == 1 and c[i] < ob.bot:
                        ob.mitigated = True
                        ob.is_breaker = True
                    elif ob.direction == -1 and c[i] > ob.top:
                        ob.mitigated = True
                        ob.is_breaker = True

            # ─── PREMIUM / DISCOUNT ───
            if not np.isnan(last_sw_h) and not np.isnan(last_sw_l):
                eq = (last_sw_h + last_sw_l) / 2
                in_premium = c[i] > eq
                in_discount = c[i] < eq
            else:
                in_premium = False
                in_discount = False
                eq = np.nan

            zone_str = "premium" if in_premium else ("discount" if in_discount else "equilibrium")

            # ─── ENTRY CONDITIONS (v1.2 FIXED) ───
            cooled = (i - last_struct_bar) >= self.cooldown

            # v1.2: Swing validation with ChoCh window
            swing_valid_bull = last_high_type == "HH" or choch_bull_active
            swing_valid_bear = last_low_type == "LL" or choch_bear_active

            # ChoCh recency
            choch_bull_recent = choch_bull_active
            choch_bear_recent = choch_bear_active

            # v1.2: Break detection with ChoCh level
            bull_broke_std = not np.isnan(last_sw_h) and c[i] > last_sw_h
            bear_broke_std = not np.isnan(last_sw_l) and c[i] < last_sw_l
            bull_broke_choch = choch_bull_active and not np.isnan(choch_bull_break) and c[i] > choch_bull_break
            bear_broke_choch = choch_bear_active and not np.isnan(choch_bear_break) and c[i] < choch_bear_break
            bull_broke = bull_broke_std or bull_broke_choch
            bear_broke = bear_broke_std or bear_broke_choch
            trend_live = 1 if bull_broke else (-1 if bear_broke else trend)

            # FVG proximity
            near_bull_fvg = False
            near_bear_fvg = False
            fvg_quality = ""
            for fvg in fvg_zones[-30:]:
                if not fvg.mitigated:
                    if fvg.direction == 1 and fvg.bot <= c[i] <= fvg.top:
                        near_bull_fvg = True
                        if fvg.fib_zone == "G":
                            fvg_quality = "G"
                    if fvg.direction == -1 and fvg.bot <= c[i] <= fvg.top:
                        near_bear_fvg = True
                        if fvg.fib_zone == "G":
                            fvg_quality = "G"

            # OB proximity
            near_bull_ob = False
            near_bear_ob = False
            for ob in ob_zones[-20:]:
                if not ob.mitigated:
                    if ob.direction == 1 and ob.bot <= c[i] <= ob.top:
                        near_bull_ob = True
                    if ob.direction == -1 and ob.bot <= c[i] <= ob.top:
                        near_bear_ob = True

            # OTE membership
            in_bull_ote = False
            in_bear_ote = False
            if not np.isnan(last_sw_h) and not np.isnan(last_sw_l):
                rng = last_sw_h - last_sw_l
                if rng > 0:
                    bull_ote_hi = last_sw_h - rng * self.ote_low
                    bull_ote_lo = last_sw_h - rng * self.ote_high
                    bear_ote_hi = last_sw_l + rng * self.ote_high
                    bear_ote_lo = last_sw_l + rng * self.ote_low
                    in_bull_ote = bull_ote_lo <= c[i] <= bull_ote_hi
                    in_bear_ote = bear_ote_lo <= c[i] <= bear_ote_hi

            # ─── BULL ENTRY ───
            bull_entry = cooled
            if self.req_choch:
                bull_entry = bull_entry and (choch_bull_recent or (trend == 1 and bos_now))
            if self.req_fvg:
                bull_entry = bull_entry and (near_bull_fvg or near_bull_ob)
            if self.req_ote:
                bull_entry = bull_entry and in_bull_ote
            if self.req_discount:
                bull_entry = bull_entry and in_discount
            if self.req_trend:
                bull_entry = bull_entry and trend_live == 1
            if self.req_swing:
                bull_entry = bull_entry and swing_valid_bull
            if self.req_break:
                bull_entry = bull_entry and bull_broke

            # Check transition (new signal, not continuation)
            if i > 0:
                bull_entry = bull_entry and not active  # Not already in trade

            # ─── BEAR ENTRY ───
            bear_entry = cooled
            if self.req_choch:
                bear_entry = bear_entry and (choch_bear_recent or (trend == -1 and bos_now))
            if self.req_fvg:
                bear_entry = bear_entry and (near_bear_fvg or near_bear_ob)
            if self.req_ote:
                bear_entry = bear_entry and in_bear_ote
            if self.req_discount:
                bear_entry = bear_entry and in_premium
            if self.req_trend:
                bear_entry = bear_entry and trend_live == -1
            if self.req_swing:
                bear_entry = bear_entry and swing_valid_bear
            if self.req_break:
                bear_entry = bear_entry and bear_broke

            if i > 0:
                bear_entry = bear_entry and not active

            # Signal cooldown
            bull_sig = bull_entry and (i - last_sig_bar > cooldown_bars or last_sig_dir != 1)
            bear_sig = bear_entry and (i - last_sig_bar > cooldown_bars or last_sig_dir != -1)

            # ─── GENERATE SIGNAL ───
            if bull_sig:
                # Calculate SL from swing low
                sl_start = max(0, i - self.sl_bars + 1)
                swing_sl = np.min(l[sl_start:i + 1])

                ep = c[i]
                tp1 = ep + self.target
                tp2 = ep + self.target * 2
                tp3 = ep + self.target * 3

                # Confluence score
                score = 0
                reason_parts = []
                if choch_bull_active:
                    score += 25
                    reason_parts.append("ChoCh")
                elif bos_now and bos_dir == 1:
                    score += 15
                    reason_parts.append("BOS")
                if fvg_quality == "G":
                    score += 20
                    reason_parts.append("FVG_Golden")
                elif near_bull_fvg:
                    score += 10
                    reason_parts.append("FVG")
                if near_bull_ob:
                    score += 10
                    reason_parts.append("OB")
                if in_bull_ote:
                    score += 10
                    reason_parts.append("OTE")
                if in_discount:
                    score += 8
                    reason_parts.append("Discount")
                if bull_broke:
                    score += 12
                    reason_parts.append("Broke")

                signals.append(CipherSignal(
                    bar=i,
                    timestamp=df.index[i] if hasattr(df.index, '__getitem__') else i,
                    direction=1,
                    entry_price=ep,
                    stop_loss=swing_sl,
                    tp1=tp1, tp2=tp2, tp3=tp3,
                    score=min(score, 100),
                    reason="+".join(reason_parts),
                    trend=trend,
                    zone=zone_str,
                    fvg_quality=fvg_quality,
                    choch_active=choch_bull_active,
                    near_ob=near_bull_ob,
                    in_ote=in_bull_ote,
                ))

                last_sig_bar = i
                last_sig_dir = 1
                if choch_bull_active:
                    choch_bull_active = False

            elif bear_sig:
                sl_start = max(0, i - self.sl_bars + 1)
                swing_sl = np.max(h[sl_start:i + 1])

                ep = c[i]
                tp1 = ep - self.target
                tp2 = ep - self.target * 2
                tp3 = ep - self.target * 3

                score = 0
                reason_parts = []
                if choch_bear_active:
                    score += 25
                    reason_parts.append("ChoCh")
                elif bos_now and bos_dir == -1:
                    score += 15
                    reason_parts.append("BOS")
                if fvg_quality == "G":
                    score += 20
                    reason_parts.append("FVG_Golden")
                elif near_bear_fvg:
                    score += 10
                    reason_parts.append("FVG")
                if near_bear_ob:
                    score += 10
                    reason_parts.append("OB")
                if in_bear_ote:
                    score += 10
                    reason_parts.append("OTE")
                if in_premium:
                    score += 8
                    reason_parts.append("Premium")
                if bear_broke:
                    score += 12
                    reason_parts.append("Broke")

                signals.append(CipherSignal(
                    bar=i,
                    timestamp=df.index[i] if hasattr(df.index, '__getitem__') else i,
                    direction=-1,
                    entry_price=ep,
                    stop_loss=swing_sl,
                    tp1=tp1, tp2=tp2, tp3=tp3,
                    score=min(score, 100),
                    reason="+".join(reason_parts),
                    trend=trend,
                    zone=zone_str,
                    fvg_quality=fvg_quality,
                    choch_active=choch_bear_active,
                    near_ob=near_bear_ob,
                    in_ote=in_bear_ote,
                ))

                last_sig_bar = i
                last_sig_dir = -1
                if choch_bear_active:
                    choch_bear_active = False

        return signals
