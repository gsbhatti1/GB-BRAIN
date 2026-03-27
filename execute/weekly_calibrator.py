"""Phase 2B weekly calibrator.

Reads observer truth tables and writes weekly decisions into SQLite.
Supports both JSON and markdown output so you can actually read it.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import json
from datetime import datetime, timedelta, timezone

from db.brain_db import connect, insert_weekly_calibration


def safe_div(num: float, den: float) -> float:
    return float(num) / float(den) if den else 0.0


def decide_action(candidate_count: int, honesty: float, precision: float, execution_ratio: float) -> tuple[str, str]:
    if candidate_count < 5:
        return "WAIT_FOR_SAMPLE", "Too few live candidates for decision."

    if honesty >= 0.35 and precision >= 0.55 and execution_ratio >= 0.50:
        return "KEEP_OR_PROMOTE", "Healthy honesty, execution ratio, and live precision."

    if honesty < 0.20 and precision >= 0.50:
        return "TIGHTEN_CONFIRMATION", "Too many false candidates despite acceptable executed precision."

    if honesty >= 0.25 and precision < 0.45:
        return "FIX_EXECUTION_OR_EXITS", "Signal survives, but execution quality is weak."

    if honesty < 0.20 and precision < 0.45:
        return "PAUSE_OR_REVIEW", "Weak honesty and weak precision."

    return "REVIEW", "Mixed live behavior needs manual review."


def run_calibration(days: int = 7) -> list[dict]:
    conn = connect()
    window_end_dt = datetime.now(timezone.utc)
    window_start_dt = window_end_dt - timedelta(days=days)
    window_start = window_start_dt.strftime("%Y-%m-%d %H:%M:%S")
    window_end = window_end_dt.strftime("%Y-%m-%d %H:%M:%S")

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
            MAX(COALESCE(sc.is_confirmed, 0)) AS is_confirmed,
            MAX(CASE WHEN sc.id IS NOT NULL AND COALESCE(sc.is_confirmed, 0) = 0 THEN 1 ELSE 0 END) AS was_invalidated
        FROM signal_candidates c
        LEFT JOIN signal_confirmations sc ON sc.candidate_id = c.id
        WHERE c.observed_at >= ? AND c.observed_at < ?
        GROUP BY c.id, c.bot_name, c.strategy_family, c.symbol, c.timeframe, c.broker, c.score
    ),
    exec_base AS (
        SELECT
            candidate_id,
            COUNT(*) AS exec_count,
            SUM(CASE WHEN status = 'closed' AND COALESCE(pnl, 0) > 0 THEN 1 ELSE 0 END) AS win_count,
            SUM(CASE WHEN status = 'closed' AND COALESCE(pnl, 0) <= 0 THEN 1 ELSE 0 END) AS loss_count
        FROM trade_executions
        WHERE opened_at >= ? AND opened_at < ?
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

    rows = [dict(row) for row in conn.execute(query, (window_start, window_end, window_start, window_end)).fetchall()]
    results: list[dict] = []

    for row in rows:
        candidate_count = row["candidate_count"] or 0
        confirmed_count = row["confirmed_count"] or 0
        invalidated_count = row["invalidated_count"] or 0
        executed_count = row["executed_count"] or 0
        win_count = row["win_count"] or 0
        loss_count = row["loss_count"] or 0

        honesty = safe_div(confirmed_count, candidate_count)
        execution_ratio = safe_div(executed_count, confirmed_count)
        precision = safe_div(win_count, executed_count)

        action, notes = decide_action(candidate_count, honesty, precision, execution_ratio)

        record = {
            **row,
            "window_start": window_start,
            "window_end": window_end,
            "honesty_ratio": round(honesty, 4),
            "false_candidate_rate": round(safe_div(invalidated_count, candidate_count), 4),
            "execution_ratio": round(execution_ratio, 4),
            "live_precision": round(precision, 4),
            "action": action,
            "notes": notes,
        }
        results.append(record)

        insert_weekly_calibration(
            conn,
            window_start=window_start,
            window_end=window_end,
            bot_name=row["bot_name"],
            strategy_family=row["strategy_family"],
            symbol=row["symbol"],
            timeframe=row["timeframe"],
            broker=row["broker"],
            candidate_count=candidate_count,
            confirmed_count=confirmed_count,
            invalidated_count=invalidated_count,
            executed_count=executed_count,
            win_count=win_count,
            loss_count=loss_count,
            honesty_ratio=honesty,
            execution_ratio=execution_ratio,
            live_precision=precision,
            avg_score=row.get("avg_score"),
            action=action,
            notes=notes,
        )

    conn.close()
    return results


def to_markdown(rows: list[dict], days: int) -> str:
    lines = [f"# GB-BRAIN Weekly Calibration ({days}d)", ""]
    if not rows:
        lines.append("_No observer rows found in this window._")
        return "\n".join(lines)

    headers = [
        "Bot", "Family", "Symbol", "TF", "Broker", "Cand",
        "Conf", "Exec", "Honesty", "Precision", "Action"
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")

    for row in rows:
        lines.append(
            "| "
            + " | ".join([
                str(row["bot_name"]),
                str(row["strategy_family"]),
                str(row["symbol"]),
                str(row["timeframe"]),
                str(row["broker"]),
                str(row["candidate_count"]),
                str(row["confirmed_count"]),
                str(row["executed_count"]),
                str(row["honesty_ratio"]),
                str(row["live_precision"]),
                str(row["action"]),
            ])
            + " |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    for row in rows:
        lines.append(
            f"- **{row['bot_name']} / {row['strategy_family']} / {row['symbol']} / {row['timeframe']}**: {row['notes']}"
        )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="GB-BRAIN weekly calibrator")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    rows = run_calibration(days=args.days)

    if args.format == "markdown":
        print(to_markdown(rows, args.days))
    else:
        print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()