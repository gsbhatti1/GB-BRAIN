"""Minimal single-position paper executor for Phase 2 shadow runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from execute.live_observer import LiveObserver


@dataclass
class OpenPaperPosition:
    execution_id: int
    candidate_id: int | None
    confirmation_id: int | None
    side: str
    entry_price: float
    stop_loss: float | None
    take_profit: float | None
    opened_bar_ts: str


class SinglePositionPaperExecutor:
    def __init__(self, observer: LiveObserver, bot_name: str, broker: str, symbol: str, timeframe: str) -> None:
        self.observer = observer
        self.bot_name = bot_name
        self.broker = broker
        self.symbol = symbol
        self.timeframe = timeframe
        self.position: OpenPaperPosition | None = None

    def on_candle(self, candle: dict[str, Any]) -> str | None:
        if self.position is None:
            return None

        high = float(candle["high"])
        low = float(candle["low"])
        ts = candle["timestamp"].isoformat()
        pos = self.position

        if pos.side == "buy":
            if pos.stop_loss is not None and low <= pos.stop_loss:
                pnl = pos.stop_loss - pos.entry_price
                self.observer.close_execution(
                    execution_id=pos.execution_id,
                    exit_price=pos.stop_loss,
                    pnl=pnl,
                    pnl_pct=(pnl / pos.entry_price) if pos.entry_price else None,
                    status="closed",
                    payload={"exit_reason": "stop_loss", "closed_bar": ts},
                )
                self.position = None
                return "stop_loss"

            if pos.take_profit is not None and high >= pos.take_profit:
                pnl = pos.take_profit - pos.entry_price
                self.observer.close_execution(
                    execution_id=pos.execution_id,
                    exit_price=pos.take_profit,
                    pnl=pnl,
                    pnl_pct=(pnl / pos.entry_price) if pos.entry_price else None,
                    status="closed",
                    payload={"exit_reason": "take_profit", "closed_bar": ts},
                )
                self.position = None
                return "take_profit"

        else:
            if pos.stop_loss is not None and high >= pos.stop_loss:
                pnl = pos.entry_price - pos.stop_loss
                self.observer.close_execution(
                    execution_id=pos.execution_id,
                    exit_price=pos.stop_loss,
                    pnl=pnl,
                    pnl_pct=(pnl / pos.entry_price) if pos.entry_price else None,
                    status="closed",
                    payload={"exit_reason": "stop_loss", "closed_bar": ts},
                )
                self.position = None
                return "stop_loss"

            if pos.take_profit is not None and low <= pos.take_profit:
                pnl = pos.entry_price - pos.take_profit
                self.observer.close_execution(
                    execution_id=pos.execution_id,
                    exit_price=pos.take_profit,
                    pnl=pnl,
                    pnl_pct=(pnl / pos.entry_price) if pos.entry_price else None,
                    status="closed",
                    payload={"exit_reason": "take_profit", "closed_bar": ts},
                )
                self.position = None
                return "take_profit"

        return None

    def on_confirmed_signal(self, signal: dict[str, Any], candidate_id: int, confirmation_id: int) -> int:
        side = "buy" if int(signal["direction"]) > 0 else "sell"
        entry_price = float(signal["entry_price"])
        stop_loss = float(signal["stop_loss"]) if signal.get("stop_loss") is not None else None
        take_profit = float(signal["tp1"] or signal["tp2"] or signal["tp3"]) if any(
            signal.get(k) is not None for k in ["tp1", "tp2", "tp3"]
        ) else None

        if self.position is not None and self.position.side != side:
            pos = self.position
            pnl = (entry_price - pos.entry_price) if pos.side == "buy" else (pos.entry_price - entry_price)
            self.observer.close_execution(
                execution_id=pos.execution_id,
                exit_price=entry_price,
                pnl=pnl,
                pnl_pct=(pnl / pos.entry_price) if pos.entry_price else None,
                status="closed",
                payload={"exit_reason": "reverse_signal", "closed_bar": signal["timestamp"]},
            )
            self.position = None

        if self.position is None:
            execution_id = self.observer.log_execution(
                bot_name=self.bot_name,
                execution_mode="paper",
                broker=self.broker,
                symbol=self.symbol,
                timeframe=self.timeframe,
                side=side,
                candidate_id=candidate_id,
                confirmation_id=confirmation_id,
                units=1.0,
                leverage=1.0,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                payload=signal,
            )
            self.position = OpenPaperPosition(
                execution_id=execution_id,
                candidate_id=candidate_id,
                confirmation_id=confirmation_id,
                side=side,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                opened_bar_ts=signal["timestamp"],
            )
            return execution_id

        return self.position.execution_id