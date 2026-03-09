"""
GB-BRAIN - Risk Manager
========================
Unified risk management for all brokers.
Protects capital with: daily loss limits, max drawdown,
cooldown after losses, position sizing, kill switch.
"""

import time
import logging
import sys
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    MAX_DAILY_LOSS_PCT, MAX_DRAWDOWN_PCT,
    MAX_POSITION_PCT, COOLDOWN_SECONDS,
)

logger = logging.getLogger("gb_brain.risk")


@dataclass
class RiskState:
    starting_balance: float = 0.0
    peak_balance: float = 0.0
    current_balance: float = 0.0
    daily_start_balance: float = 0.0
    daily_pnl: float = 0.0
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    consecutive_losses: int = 0
    max_consecutive_losses: int = 0
    last_loss_time: float = 0.0
    is_halted: bool = False
    halt_reason: str = ""


class RiskManager:
    """Enforces risk limits across all brokers. Capital is priority."""

    def __init__(self,
                 max_daily_loss_pct=MAX_DAILY_LOSS_PCT,
                 max_drawdown_pct=MAX_DRAWDOWN_PCT,
                 max_position_pct=MAX_POSITION_PCT,
                 cooldown_seconds=COOLDOWN_SECONDS):
        self.max_daily_loss = max_daily_loss_pct
        self.max_drawdown = max_drawdown_pct
        self.max_position = max_position_pct
        self.cooldown = cooldown_seconds
        self.state = RiskState()
        self._daily_reset_time = time.time()

    def initialize(self, balance):
        """Call on startup with account balance."""
        self.state.starting_balance = balance
        self.state.peak_balance = balance
        self.state.current_balance = balance
        self.state.daily_start_balance = balance
        self._daily_reset_time = time.time()
        logger.info(f"Risk manager initialized: ${balance:.2f}")

    def update_balance(self, balance):
        """Update after each trade or check."""
        self.state.current_balance = balance
        if balance > self.state.peak_balance:
            self.state.peak_balance = balance

        # Daily reset every 24h
        if time.time() - self._daily_reset_time > 86400:
            self.state.daily_start_balance = balance
            self.state.daily_pnl = 0.0
            self._daily_reset_time = time.time()

        self.state.daily_pnl = balance - self.state.daily_start_balance

    def can_trade(self):
        """Check all risk conditions. Returns (allowed, reason)."""
        s = self.state

        if s.is_halted:
            return False, f"HALTED: {s.halt_reason}"

        # Daily loss limit
        if s.daily_start_balance > 0:
            daily_loss = abs(min(0, s.daily_pnl)) / s.daily_start_balance
            if daily_loss >= self.max_daily_loss:
                s.is_halted = True
                s.halt_reason = f"Daily loss {daily_loss*100:.1f}% >= {self.max_daily_loss*100:.0f}%"
                return False, s.halt_reason

        # Max drawdown from peak
        if s.peak_balance > 0:
            dd = 1 - (s.current_balance / s.peak_balance)
            if dd >= self.max_drawdown:
                s.is_halted = True
                s.halt_reason = f"Drawdown {dd*100:.1f}% >= {self.max_drawdown*100:.0f}%"
                return False, s.halt_reason

        # Cooldown after loss
        if s.last_loss_time > 0:
            elapsed = time.time() - s.last_loss_time
            wait = self.cooldown * max(1, s.consecutive_losses)
            if elapsed < wait:
                return False, f"Cooldown: {wait - elapsed:.0f}s left"

        return True, "OK"

    def record_trade(self, pnl, side="buy"):
        """Record completed trade."""
        s = self.state
        s.total_trades += 1

        if pnl >= 0:
            s.wins += 1
            s.consecutive_losses = 0
        else:
            s.losses += 1
            s.consecutive_losses += 1
            s.max_consecutive_losses = max(s.max_consecutive_losses, s.consecutive_losses)
            s.last_loss_time = time.time()

    def position_size(self, balance, price, leverage=1):
        """Calculate safe position size in units."""
        margin = balance * self.max_position

        # Reduce after consecutive losses
        if self.state.consecutive_losses >= 2:
            reduction = 0.5 ** self.state.consecutive_losses
            margin *= max(reduction, 0.25)

        notional = margin * leverage
        units = notional / price if price > 0 else 0
        return round(units, 4)

    def reset_halt(self):
        """Manual reset. Use with caution."""
        self.state.is_halted = False
        self.state.halt_reason = ""
        self.state.consecutive_losses = 0
        logger.info("Risk halt manually reset")

    def report(self):
        """Quick status string."""
        s = self.state
        wr = (s.wins / max(s.total_trades, 1)) * 100
        dd = (1 - s.current_balance / max(s.peak_balance, 1)) * 100
        pnl = s.current_balance - s.starting_balance
        return (
            f"Balance: ${s.current_balance:.2f} | "
            f"PnL: ${pnl:+.2f} | DD: {dd:.1f}% | "
            f"Trades: {s.total_trades} (W:{s.wins} L:{s.losses}) | "
            f"WinRate: {wr:.0f}% | "
            f"{'HALTED' if s.is_halted else 'ACTIVE'}"
        )
