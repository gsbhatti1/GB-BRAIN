"""Phase 2 live observer for candidate / confirmed / executed truth."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import argparse
import json
from datetime import datetime, timedelta, timezone

from db.brain_db import (
    connect,
    init_db,
    insert_signal_candidate,
    insert_signal_confirmation,
    insert_trade_execution,
    close_trade_execution,
)
from config.settings import LIVE_OBSERVER_DEFAULT_DAYS


class LiveObserver:
    def __init__(self, conn=None):
        self.conn = conn or connect()

    def log_candidate(
        self,
        *,
        bot_name: str,
        strategy_family: str,
        symbol: str,
        timeframe: str,
        broker: str,
        signal: dict,
        status: str = "candidate",
    ) -> int:
        return insert_signal_candidate(
            self.conn,
            bot_name=bot_name,
            strategy_family=strategy_family,
            symbol=symbol,
            timeframe=timeframe,
            broker=broker,
            bar_timestamp=str(signal["timestamp"]),
            direction=int(signal["direction"]),
            entry_price=signal.get("entry_price"),
            stop_loss=signal.get("stop_loss"),
            tp1=signal.get("tp1"),
            tp2=signal.get("tp2"),
            tp3=signal.get("tp3"),
            score=signal.get("score"),
            source=signal.get("source"),
            reason=signal.get("reason"),
            preset_version="phase2",
            status=status,
            payload=signal,
        )

    def log_confirmation(
        self,
        *,
        candidate_id: int,
        confirmed: bool,
        confirmation_bar_ts: str | None = None,
        invalidation_reason: str | None = None,
        payload: dict | None = None,
    ) -> int:
        return insert_signal_confirmation(
            self.conn,
            candidate_id=candidate_id,
            is_confirmed=confirmed,
            confirmation_bar_ts=confirmation_bar_ts,
            invalidation_reason=invalidation_reason,
            payload=payload,
        )

    def log_execution(
        self,
        *,
        bot_name: str,
        execution_mode: str,
        broker: str,
        symbol: str,
        timeframe: str,
        side: str,
        candidate_id: int | None = None,
        confirmation_id: int | None = None,
        units: float | None = None,
        leverage: float = 1.0,
        entry_price: float | None = None,
        stop_loss: float | None = None,
        take_profit: float | None = None,
        payload: dict | None = None,
    ) -> int:
        return insert_trade_execution(
            self.conn,
            bot_name=bot_name,
            execution_mode=execution_mode,
            broker=broker,
            symbol=symbol,
            timeframe=timeframe,
            side=side,
            candidate_id=candidate_id,
            confirmation_id=confirmation_id,
            units=units,
            leverage=leverage,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            payload=payload,
        )

    def close_execution(
        self,
        *,
        execution_id: int,
        exit_price: float | None = None,
        fees: float = 0.0,
        pnl: float | None = None,
        pnl_pct: float | None = None,
        status: str = "closed",
        payload: dict | None = None,
    ) -> None:
        close_trade_execution(
            self.conn,
            execution_id=execution_id,
            exit_price=exit_price,
            fees=fees,
            pnl=pnl,
            pnl_pct=pnl_pct,
            status=status,
            payload=payload,
        )

    def summary(self, days: int = LIVE_OBSERVER_DEFAULT_DAYS) -> dict:
        since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

        query = """
        WITH candidate_base AS (
            SELECT
                c.id,
                c.bot_name,
                c.strategy_family,
                c.symbol,
                c.timeframe,
                c.broker,
                c.score,
                MAX(CASE WHEN COALESCE(sc.is_confirmed, 0) = 1 THEN 1 ELSE 0 END) AS is_confirmed,
                MAX(CASE WHEN sc.id IS NOT NULL AND COALESCE(sc.is_confirmed, 0) = 0 THEN 1 ELSE 0 END) AS was_invalidated
            FROM signal_candidates c
            LEFT JOIN signal_confirmations sc ON sc.candidate_id = c.id
            WHERE c.observed_at >= ?
            GROUP BY c.id, c.bot_name, c.strategy_family, c.symbol, c.timeframe, c.broker, c.score
        ),
        exec_base AS (
            SELECT
                candidate_id,
                COUNT(*) AS exec_count,
                SUM(CASE WHEN status = 'closed' AND COALESCE(pnl, 0) > 0 THEN 1 ELSE 0 END) AS win_count,
                SUM(CASE WHEN status = 'closed' AND COALESCE(pnl, 0) <= 0 THEN 1 ELSE 0 END) AS loss_count
            FROM trade_executions
            WHERE opened_at >= ?
            GROUP BY candidate_id
        )
        SELECT
            cb.bot_name,
            cb.strategy_family,
            cb.symbol,
            cb.timeframe,
            cb.broker,
            COUNT(*) AS candidate_count,
            SUM(CASE WHEN cb.is_confirmed = 1 THEN 1 ELSE 0 END) AS confirmed_count,
            SUM(CASE WHEN cb.was_invalidated = 1 THEN 1 ELSE 0 END) AS invalidated_count,
            SUM(COALESCE(eb.exec_count, 0)) AS executed_count,
            SUM(COALESCE(eb.win_count, 0)) AS win_count,
            SUM(COALESCE(eb.loss_count, 0)) AS loss_count,
            ROUND(AVG(cb.score), 2) AS avg_score
        FROM candidate_base cb
        LEFT JOIN exec_base eb ON eb.candidate_id = cb.id
        GROUP BY cb.bot_name, cb.strategy_family, cb.symbol, cb.timeframe, cb.broker
        ORDER BY candidate_count DESC, cb.bot_name, cb.strategy_family, cb.symbol, cb.timeframe
        """

        rows = [dict(row) for row in self.conn.execute(query, (since, since)).fetchall()]

        for row in rows:
            cand = row["candidate_count"] or 0
            conf = row["confirmed_count"] or 0
            inval = row["invalidated_count"] or 0
            exe = row["executed_count"] or 0
            wins = row["win_count"] or 0
            row["honesty_ratio"] = round(conf / cand, 4) if cand else 0.0
            row["false_candidate_rate"] = round(inval / cand, 4) if cand else 0.0
            row["execution_ratio"] = round(exe / conf, 4) if conf else 0.0
            row["live_precision"] = round(wins / exe, 4) if exe else 0.0

        return {"since": since, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description="GB-BRAIN live observer")
    parser.add_argument("--init", action="store_true", help="Initialize DB tables")
    parser.add_argument("--summary", action="store_true", help="Show grouped summary")
    parser.add_argument("--days", type=int, default=LIVE_OBSERVER_DEFAULT_DAYS)
    args = parser.parse_args()

    if args.init:
        init_db()

    obs = LiveObserver()
    if args.summary or args.init:
        result = obs.summary(days=args.days)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()