"""
GB-BRAIN — Monitor Dashboard
==============================
Flask web dashboard showing live system status.
Access at http://localhost:5001 (separate port from webhook on 5000)

Pages:
  /           → Overview: kill switch state, active lanes, today's stats
  /gems       → Top GEM strategies sorted by composite score
  /signals    → Recent observed signals from all lanes
  /trades     → Recent paper/demo/live trades with P&L
  /health     → Health check results
  /calibration → Latest calibration report
  /api/status → JSON status endpoint for monitoring tools

Usage:
    python monitor/dashboard.py
    python monitor/dashboard.py --port 5001 --host 0.0.0.0
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, date

from flask import Flask, jsonify, render_template_string

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "trading.db")
KILL_SWITCH_PATH = os.path.join(BASE_DIR, "db", "kill_switch.json")
CALIBRATION_PATH = os.path.join(BASE_DIR, "db", "calibration_report.json")


# ---------------------------------------------------------------------------
# Health Check (imported gracefully — may not exist yet)
# ---------------------------------------------------------------------------

try:
    import sys
    sys.path.insert(0, BASE_DIR)
    from health_check import HealthCheck  # type: ignore
    _HEALTH_CHECK_AVAILABLE = True
except ImportError:
    _HEALTH_CHECK_AVAILABLE = False


# ---------------------------------------------------------------------------
# DashboardData
# ---------------------------------------------------------------------------

class DashboardData:
    """Reads live data from SQLite and supporting JSON files."""

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_conn(self):
        """Return a read-only SQLite connection (row_factory enabled)."""
        if not os.path.exists(DB_PATH):
            return None
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    def _query(self, sql: str, params: tuple = ()) -> list:
        """Execute a SELECT and return list-of-dicts; empty list on any error."""
        conn = self._get_conn()
        if conn is None:
            return []
        try:
            cur = conn.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
            return rows
        except sqlite3.OperationalError:
            return []
        finally:
            conn.close()

    def _scalar(self, sql: str, params: tuple = (), default=0):
        """Return first column of first row, or *default* on error."""
        conn = self._get_conn()
        if conn is None:
            return default
        try:
            cur = conn.execute(sql, params)
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else default
        except sqlite3.OperationalError:
            return default
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Kill switch
    # ------------------------------------------------------------------

    def get_kill_switch_state(self) -> dict:
        """Read db/kill_switch.json and return its contents as a dict."""
        if not os.path.exists(KILL_SWITCH_PATH):
            return {
                "active": False,
                "reason": "File not found",
                "timestamp": None,
                "source": "unknown",
            }
        try:
            with open(KILL_SWITCH_PATH) as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, OSError) as exc:
            return {
                "active": False,
                "reason": f"Read error: {exc}",
                "timestamp": None,
                "source": "error",
            }

    # ------------------------------------------------------------------
    # Overview
    # ------------------------------------------------------------------

    def get_overview(self) -> dict:
        """Aggregate top-level metrics for the overview page."""
        today = date.today().isoformat()

        kill_switch = self.get_kill_switch_state()

        signals_today = self._scalar(
            "SELECT COUNT(*) FROM observed_signals WHERE DATE(timestamp) = ?",
            (today,),
        )

        trades_today = self._scalar(
            "SELECT COUNT(*) FROM live_trades WHERE DATE(opened_at) = ?",
            (today,),
        )

        pnl_today = self._scalar(
            "SELECT ROUND(SUM(pnl), 2) FROM live_trades WHERE DATE(opened_at) = ?",
            (today,),
            default=0.0,
        )

        active_lanes = self._scalar(
            "SELECT COUNT(DISTINCT lane) FROM observed_signals WHERE DATE(timestamp) = ?",
            (today,),
        )

        recent_signals = self._query(
            """
            SELECT timestamp, lane, symbol, strategy_name, direction,
                   entry_price, stop_loss, composite_score, reason
            FROM   observed_signals
            ORDER  BY timestamp DESC
            LIMIT  10
            """,
        )

        recent_trades = self._query(
            """
            SELECT opened_at, symbol, broker, side, entry_price,
                   exit_price, pnl, risk_reward, status
            FROM   live_trades
            ORDER  BY opened_at DESC
            LIMIT  10
            """,
        )

        return {
            "kill_switch": kill_switch,
            "active_lanes": active_lanes,
            "signals_today": signals_today,
            "trades_today": trades_today,
            "pnl_today": pnl_today,
            "recent_signals": recent_signals,
            "recent_trades": recent_trades,
            "as_of": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

    # ------------------------------------------------------------------
    # GEMs
    # ------------------------------------------------------------------

    def get_gems(self) -> list:
        """Return top 50 GEM strategies sorted by composite_score DESC."""
        return self._query(
            """
            SELECT strategy_name, symbol, timeframe,
                   win_rate, profit_factor, avg_return,
                   composite_score, status
            FROM   backtest_results
            WHERE  status = 'GEM'
            ORDER  BY composite_score DESC
            LIMIT  50
            """,
        )

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def get_signals(self, limit: int = 100) -> list:
        """Return *limit* most recent rows from observed_signals."""
        return self._query(
            """
            SELECT timestamp, lane, symbol, strategy_name, direction,
                   entry_price, stop_loss, composite_score, reason
            FROM   observed_signals
            ORDER  BY timestamp DESC
            LIMIT  ?
            """,
            (limit,),
        )

    # ------------------------------------------------------------------
    # Trades
    # ------------------------------------------------------------------

    def get_trades(self, limit: int = 100) -> list:
        """Return *limit* most recent rows from live_trades."""
        return self._query(
            """
            SELECT opened_at, symbol, broker, side, entry_price,
                   exit_price, pnl, risk_reward, status
            FROM   live_trades
            ORDER  BY opened_at DESC
            LIMIT  ?
            """,
            (limit,),
        )

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def get_health(self) -> dict:
        """Run all health checks and return results dict."""
        if not _HEALTH_CHECK_AVAILABLE:
            return {
                "available": False,
                "message": "HealthCheck module not found. "
                           "Ensure health_check.py is in the project root.",
                "checks": [],
                "overall": "UNKNOWN",
            }
        try:
            results = HealthCheck.run_all()
            return {"available": True, "results": results}
        except Exception as exc:  # noqa: BLE001
            return {
                "available": False,
                "message": f"HealthCheck failed: {exc}",
                "checks": [],
                "overall": "ERROR",
            }

    # ------------------------------------------------------------------
    # Calibration
    # ------------------------------------------------------------------

    def get_calibration(self) -> dict:
        """Read the latest calibration report JSON."""
        if not os.path.exists(CALIBRATION_PATH):
            return {
                "available": False,
                "message": "Calibration report not found at db/calibration_report.json. "
                           "Run the calibration pipeline first.",
            }
        try:
            with open(CALIBRATION_PATH) as f:
                data = json.load(f)
            data["available"] = True
            return data
        except (json.JSONDecodeError, OSError) as exc:
            return {"available": False, "message": f"Read error: {exc}"}


# ---------------------------------------------------------------------------
# Shared HTML helpers
# ---------------------------------------------------------------------------

DARK_STYLES = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    font-size: 14px;
    line-height: 1.5;
}
a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Navbar ── */
.navbar {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 0 24px;
    display: flex;
    align-items: center;
    height: 52px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.navbar .brand {
    font-size: 16px;
    font-weight: 700;
    color: #00ff88;
    letter-spacing: 0.05em;
    margin-right: 32px;
    text-decoration: none;
}
.navbar .brand:hover { text-decoration: none; opacity: 0.85; }
.navbar .nav-links {
    display: flex;
    gap: 4px;
    flex: 1;
}
.navbar .nav-link {
    color: #8b949e;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    transition: color 0.15s, background 0.15s;
}
.navbar .nav-link:hover {
    color: #c9d1d9;
    background: #21262d;
    text-decoration: none;
}
.navbar .nav-link.active {
    color: #c9d1d9;
    background: #21262d;
}
.navbar .timestamp {
    font-size: 11px;
    color: #484f58;
    margin-left: auto;
}

/* ── Page wrapper ── */
.page { padding: 28px 32px; max-width: 1400px; margin: 0 auto; }
.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #e6edf3;
    margin-bottom: 24px;
}

/* ── Stat cards ── */
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px;
}
.card .card-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8b949e;
    margin-bottom: 8px;
}
.card .card-value {
    font-size: 28px;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1.1;
}
.card .card-sub {
    font-size: 12px;
    color: #8b949e;
    margin-top: 4px;
}

/* ── Color tokens ── */
.green  { color: #00ff88; }
.red    { color: #ff4444; }
.gold   { color: #ffd700; }
.muted  { color: #8b949e; }
.warn   { color: #f0a500; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.badge-green  { background: rgba(0,255,136,0.12); color: #00ff88; }
.badge-red    { background: rgba(255,68,68,0.12);  color: #ff4444; }
.badge-gold   { background: rgba(255,215,0,0.12);  color: #ffd700; }
.badge-muted  { background: rgba(139,148,158,0.12); color: #8b949e; }
.badge-blue   { background: rgba(88,166,255,0.12); color: #58a6ff; }

/* ── Section label ── */
.section-label {
    font-size: 13px;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
    margin-top: 28px;
}

/* ── Tables ── */
.table-wrap {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    overflow: auto;
    margin-bottom: 28px;
}
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
thead tr {
    border-bottom: 1px solid #30363d;
}
thead th {
    padding: 10px 14px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8b949e;
    white-space: nowrap;
}
tbody tr {
    border-bottom: 1px solid #21262d;
    transition: background 0.1s;
}
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: #21262d; }
tbody td {
    padding: 9px 14px;
    color: #c9d1d9;
    white-space: nowrap;
}

/* ── Empty state ── */
.empty-state {
    padding: 48px 24px;
    text-align: center;
    color: #484f58;
    font-size: 14px;
}
.empty-state .empty-title {
    font-size: 16px;
    color: #8b949e;
    margin-bottom: 8px;
    font-weight: 600;
}

/* ── Health checks ── */
.health-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
}
.health-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 18px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.health-icon {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-top: 4px;
    flex-shrink: 0;
}
.health-ok     { background: #00ff88; box-shadow: 0 0 6px rgba(0,255,136,0.5); }
.health-warn   { background: #f0a500; box-shadow: 0 0 6px rgba(240,165,0,0.5); }
.health-error  { background: #ff4444; box-shadow: 0 0 6px rgba(255,68,68,0.5); }
.health-info   { background: #58a6ff; }
.health-name   { font-weight: 600; color: #e6edf3; font-size: 13px; }
.health-detail { font-size: 12px; color: #8b949e; margin-top: 2px; }

/* ── JSON block ── */
.json-block {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 12px;
    color: #79c0ff;
    overflow: auto;
    white-space: pre;
    line-height: 1.7;
}

/* ── Kill switch banner ── */
.ks-banner {
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 24px;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.ks-active   { background: rgba(255,68,68,0.12);  border: 1px solid rgba(255,68,68,0.35);  color: #ff4444; }
.ks-inactive { background: rgba(0,255,136,0.08);  border: 1px solid rgba(0,255,136,0.25);  color: #00ff88; }
.ks-dot {
    width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}
.ks-active .ks-dot   { background: #ff4444; box-shadow: 0 0 8px rgba(255,68,68,0.7); }
.ks-inactive .ks-dot { background: #00ff88; box-shadow: 0 0 8px rgba(0,255,136,0.7); }
"""

NAVBAR_TEMPLATE = """
<nav class="navbar">
    <a href="/" class="brand">&#9670; GB-BRAIN</a>
    <div class="nav-links">
        <a href="/"            class="nav-link {cls_overview}">Overview</a>
        <a href="/gems"        class="nav-link {cls_gems}">GEMs</a>
        <a href="/signals"     class="nav-link {cls_signals}">Signals</a>
        <a href="/trades"      class="nav-link {cls_trades}">Trades</a>
        <a href="/health"      class="nav-link {cls_health}">Health</a>
        <a href="/calibration" class="nav-link {cls_calibration}">Calibration</a>
    </div>
    <span class="timestamp">Updated: {ts}</span>
</nav>
"""

BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="30">
    <title>{title} — GB-BRAIN Monitor</title>
    <style>{styles}</style>
</head>
<body>
{navbar}
<div class="page">
{body}
</div>
</body>
</html>"""


def render_page(title: str, body: str, active: str) -> str:
    """Wrap *body* HTML in the full page shell."""
    ts = datetime.utcnow().strftime("%H:%M:%S UTC")
    pages = ["overview", "gems", "signals", "trades", "health", "calibration"]
    cls = {p: "active" if p == active else "" for p in pages}
    navbar = NAVBAR_TEMPLATE.format(
        cls_overview=cls["overview"],
        cls_gems=cls["gems"],
        cls_signals=cls["signals"],
        cls_trades=cls["trades"],
        cls_health=cls["health"],
        cls_calibration=cls["calibration"],
        ts=ts,
    )
    return BASE_TEMPLATE.format(
        title=title,
        styles=DARK_STYLES,
        navbar=navbar,
        body=body,
    )


def _fmt_float(val, decimals: int = 2, suffix: str = "") -> str:
    """Format a numeric value or return '—'."""
    if val is None:
        return "—"
    try:
        return f"{float(val):.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return str(val)


def _pnl_cell(val) -> str:
    """Colour-coded P&L cell content."""
    if val is None:
        return "<span class='muted'>—</span>"
    try:
        fval = float(val)
    except (TypeError, ValueError):
        return str(val)
    cls = "green" if fval >= 0 else "red"
    sign = "+" if fval > 0 else ""
    return f"<span class='{cls}'>{sign}{fval:.2f}</span>"


def _dir_badge(direction) -> str:
    if direction is None:
        return "<span class='muted'>—</span>"
    d = str(direction).upper()
    if d in ("BUY", "LONG"):
        return "<span class='badge badge-green'>LONG</span>"
    if d in ("SELL", "SHORT"):
        return "<span class='badge badge-red'>SHORT</span>"
    return f"<span class='badge badge-muted'>{d}</span>"


def _status_badge(status) -> str:
    if status is None:
        return "<span class='muted'>—</span>"
    s = str(status).upper()
    mapping = {
        "OPEN":   "badge-blue",
        "CLOSED": "badge-muted",
        "WIN":    "badge-green",
        "LOSS":   "badge-red",
        "GEM":    "badge-gold",
        "PASS":   "badge-muted",
        "WATCH":  "badge-blue",
    }
    css = mapping.get(s, "badge-muted")
    return f"<span class='badge {css}'>{s}</span>"


def _empty(msg: str = "No data available yet.") -> str:
    return (
        "<div class='empty-state'>"
        f"<div class='empty-title'>No Records</div>{msg}"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------------

app = Flask(__name__)
data = DashboardData()


# ------------------------------------------------------------------
# / — Overview
# ------------------------------------------------------------------

@app.route("/")
def overview():
    ov = data.get_overview()
    ks = ov["kill_switch"]
    ks_active = ks.get("active", False)
    ks_cls = "ks-active" if ks_active else "ks-inactive"
    ks_label = "KILL SWITCH ACTIVE" if ks_active else "System Operational"
    ks_reason = ks.get("reason", "")
    ks_ts = ks.get("timestamp", "")
    ks_detail = ""
    if ks_active and ks_reason:
        ks_detail = f" &mdash; {ks_reason}"
    if ks_ts:
        ks_detail += f" <span class='muted'>[{ks_ts}]</span>"

    pnl = ov["pnl_today"]
    pnl_cls = "green" if (pnl or 0) >= 0 else "red"
    pnl_sign = "+" if (pnl or 0) > 0 else ""

    body = f"""
<h1 class="page-title">System Overview</h1>

<div class="ks-banner {ks_cls}">
    <span class="ks-dot"></span>
    {ks_label}{ks_detail}
</div>

<div class="cards">
    <div class="card">
        <div class="card-label">Active Lanes</div>
        <div class="card-value">{ov['active_lanes']}</div>
        <div class="card-sub">lanes with signals today</div>
    </div>
    <div class="card">
        <div class="card-label">Signals Today</div>
        <div class="card-value">{ov['signals_today']}</div>
        <div class="card-sub">observed signals</div>
    </div>
    <div class="card">
        <div class="card-label">Trades Today</div>
        <div class="card-value">{ov['trades_today']}</div>
        <div class="card-sub">executed trades</div>
    </div>
    <div class="card">
        <div class="card-label">P&amp;L Today</div>
        <div class="card-value {pnl_cls}">{pnl_sign}{_fmt_float(pnl)}</div>
        <div class="card-sub">sum of closed trades</div>
    </div>
</div>

<div class="section-label">Recent Signals</div>
{_signals_table(ov['recent_signals'])}

<div class="section-label">Recent Trades</div>
{_trades_table(ov['recent_trades'])}
"""
    return render_template_string(render_page("Overview", body, "overview"))


# ------------------------------------------------------------------
# /gems
# ------------------------------------------------------------------

@app.route("/gems")
def gems():
    rows = data.get_gems()
    if not rows:
        table = _empty(
            "No GEM strategies found. Run the backtest pipeline and mark "
            "qualifying strategies as status='GEM' in backtest_results."
        )
    else:
        rows_html = ""
        for i, r in enumerate(rows, 1):
            score = r.get("composite_score")
            score_cell = (
                f"<span class='gold'>{_fmt_float(score)}</span>"
                if score is not None
                else "<span class='muted'>—</span>"
            )
            rows_html += f"""
<tr>
    <td class="muted" style="width:36px">{i}</td>
    <td style="font-weight:600;color:#e6edf3">{r.get('strategy_name','—')}</td>
    <td>{r.get('symbol','—')}</td>
    <td class="muted">{r.get('timeframe','—')}</td>
    <td>{_fmt_float(r.get('win_rate'), 1, '%')}</td>
    <td>{_fmt_float(r.get('profit_factor'))}</td>
    <td>{_fmt_float(r.get('avg_return'), 2, '%')}</td>
    <td>{score_cell}</td>
    <td>{_status_badge(r.get('status'))}</td>
</tr>"""
        table = f"""
<div class="table-wrap">
<table>
<thead><tr>
    <th>#</th>
    <th>Name</th>
    <th>Symbol</th>
    <th>Timeframe</th>
    <th>Win Rate</th>
    <th>P/F</th>
    <th>Return</th>
    <th>Score</th>
    <th>Status</th>
</tr></thead>
<tbody>{rows_html}</tbody>
</table>
</div>"""

    body = f"""
<h1 class="page-title">GEM Strategies <span class="muted" style="font-size:16px;font-weight:400">({len(rows)} found)</span></h1>
{table}
"""
    return render_template_string(render_page("GEM Strategies", body, "gems"))


# ------------------------------------------------------------------
# /signals
# ------------------------------------------------------------------

def _signals_table(rows: list) -> str:
    if not rows:
        return _empty(
            "No signals recorded yet. Signals appear here once the lane "
            "engines start generating observations."
        )
    rows_html = ""
    for r in rows:
        rows_html += f"""
<tr>
    <td class="muted">{r.get('timestamp','—')}</td>
    <td>{r.get('lane','—')}</td>
    <td style="font-weight:600">{r.get('symbol','—')}</td>
    <td>{r.get('strategy_name','—')}</td>
    <td>{_dir_badge(r.get('direction'))}</td>
    <td>{_fmt_float(r.get('entry_price'))}</td>
    <td>{_fmt_float(r.get('stop_loss'))}</td>
    <td><span class="gold">{_fmt_float(r.get('composite_score'))}</span></td>
    <td class="muted" style="max-width:240px;overflow:hidden;text-overflow:ellipsis">{r.get('reason','—')}</td>
</tr>"""
    return f"""
<div class="table-wrap">
<table>
<thead><tr>
    <th>Time</th>
    <th>Lane</th>
    <th>Symbol</th>
    <th>Strategy</th>
    <th>Direction</th>
    <th>Entry</th>
    <th>Stop Loss</th>
    <th>Score</th>
    <th>Reason</th>
</tr></thead>
<tbody>{rows_html}</tbody>
</table>
</div>"""


@app.route("/signals")
def signals():
    rows = data.get_signals(limit=100)
    body = f"""
<h1 class="page-title">Observed Signals <span class="muted" style="font-size:16px;font-weight:400">(last {len(rows)})</span></h1>
{_signals_table(rows)}
"""
    return render_template_string(render_page("Signals", body, "signals"))


# ------------------------------------------------------------------
# /trades
# ------------------------------------------------------------------

def _trades_table(rows: list) -> str:
    if not rows:
        return _empty(
            "No trades recorded yet. Trades appear here once the execution "
            "engine places its first order."
        )
    rows_html = ""
    for r in rows:
        rows_html += f"""
<tr>
    <td class="muted">{r.get('opened_at','—')}</td>
    <td style="font-weight:600">{r.get('symbol','—')}</td>
    <td>{r.get('broker','—')}</td>
    <td>{_dir_badge(r.get('side'))}</td>
    <td>{_fmt_float(r.get('entry_price'))}</td>
    <td>{_fmt_float(r.get('exit_price'))}</td>
    <td>{_pnl_cell(r.get('pnl'))}</td>
    <td>{_fmt_float(r.get('risk_reward'))}</td>
    <td>{_status_badge(r.get('status'))}</td>
</tr>"""
    return f"""
<div class="table-wrap">
<table>
<thead><tr>
    <th>Time</th>
    <th>Symbol</th>
    <th>Broker</th>
    <th>Side</th>
    <th>Entry</th>
    <th>Exit</th>
    <th>P&amp;L</th>
    <th>R:R</th>
    <th>Status</th>
</tr></thead>
<tbody>{rows_html}</tbody>
</table>
</div>"""


@app.route("/trades")
def trades():
    rows = data.get_trades(limit=100)
    body = f"""
<h1 class="page-title">Trade Log <span class="muted" style="font-size:16px;font-weight:400">(last {len(rows)})</span></h1>
{_trades_table(rows)}
"""
    return render_template_string(render_page("Trades", body, "trades"))


# ------------------------------------------------------------------
# /health
# ------------------------------------------------------------------

@app.route("/health")
def health():
    result = data.get_health()
    if not result.get("available"):
        body = f"""
<h1 class="page-title">System Health</h1>
<div class="card" style="max-width:560px">
    <div class="card-label">Health Check Unavailable</div>
    <div style="color:#8b949e;margin-top:8px;font-size:13px">{result.get('message','')}</div>
</div>
"""
    else:
        checks = result.get("results", {})
        if isinstance(checks, dict):
            items = checks.items()
        else:
            items = [(str(i), c) for i, c in enumerate(checks)]

        cards_html = ""
        for name, info in items:
            if isinstance(info, dict):
                ok = info.get("ok", info.get("status", "unknown"))
                detail = info.get("detail", info.get("message", ""))
            else:
                ok = bool(info)
                detail = str(info)

            if ok is True or str(ok).upper() in ("OK", "PASS", "HEALTHY"):
                icon_cls = "health-ok"
                label_cls = "green"
                label = "OK"
            elif str(ok).upper() in ("WARN", "WARNING", "DEGRADED"):
                icon_cls = "health-warn"
                label_cls = "warn"
                label = "WARN"
            elif ok is False or str(ok).upper() in ("ERROR", "FAIL", "CRITICAL"):
                icon_cls = "health-error"
                label_cls = "red"
                label = "FAIL"
            else:
                icon_cls = "health-info"
                label_cls = "muted"
                label = str(ok).upper()

            cards_html += f"""
<div class="health-card">
    <span class="health-icon {icon_cls}"></span>
    <div>
        <div class="health-name">{name}</div>
        <div class="health-detail {label_cls}">{label}</div>
        <div class="health-detail">{detail}</div>
    </div>
</div>"""

        body = f"""
<h1 class="page-title">System Health</h1>
<div class="health-grid">
{cards_html}
</div>
"""
    return render_template_string(render_page("Health", body, "health"))


# ------------------------------------------------------------------
# /calibration
# ------------------------------------------------------------------

@app.route("/calibration")
def calibration():
    cal = data.get_calibration()
    if not cal.get("available"):
        body = f"""
<h1 class="page-title">Calibration Report</h1>
<div class="card" style="max-width:560px">
    <div class="card-label">Report Unavailable</div>
    <div style="color:#8b949e;margin-top:8px;font-size:13px">{cal.get('message','')}</div>
</div>
"""
    else:
        # Strip the 'available' helper key before displaying JSON
        display = {k: v for k, v in cal.items() if k != "available"}

        # Try to render a summary if the report has known keys
        summary_cards = ""
        if "generated_at" in display or "timestamp" in display:
            ts_val = display.get("generated_at") or display.get("timestamp", "—")
            summary_cards += f"""
<div class="card" style="max-width:220px">
    <div class="card-label">Generated At</div>
    <div class="card-value" style="font-size:16px">{ts_val}</div>
</div>"""
        if "total_strategies" in display:
            summary_cards += f"""
<div class="card" style="max-width:220px">
    <div class="card-label">Strategies Evaluated</div>
    <div class="card-value">{display['total_strategies']}</div>
</div>"""
        if "gems_found" in display or "gem_count" in display:
            gem_cnt = display.get("gems_found") or display.get("gem_count", "—")
            summary_cards += f"""
<div class="card" style="max-width:220px">
    <div class="card-label">GEMs Found</div>
    <div class="card-value gold">{gem_cnt}</div>
</div>"""

        cards_row = f"<div class='cards'>{summary_cards}</div>" if summary_cards else ""

        body = f"""
<h1 class="page-title">Calibration Report</h1>
{cards_row}
<div class="section-label">Full Report (JSON)</div>
<div class="json-block">{json.dumps(display, indent=2, default=str)}</div>
"""
    return render_template_string(render_page("Calibration", body, "calibration"))


# ------------------------------------------------------------------
# /api/status  (JSON endpoint)
# ------------------------------------------------------------------

@app.route("/api/status")
def api_status():
    today = date.today().isoformat()
    ks = data.get_kill_switch_state()
    signals_1h = data._scalar(
        """
        SELECT COUNT(*) FROM observed_signals
        WHERE timestamp >= datetime('now', '-1 hour')
        """,
    )
    trades_today = data._scalar(
        "SELECT COUNT(*) FROM live_trades WHERE DATE(opened_at) = ?",
        (today,),
    )
    active_lanes = data._scalar(
        "SELECT COUNT(DISTINCT lane) FROM observed_signals WHERE DATE(timestamp) = ?",
        (today,),
    )
    pnl_today = data._scalar(
        "SELECT ROUND(SUM(pnl), 2) FROM live_trades WHERE DATE(opened_at) = ?",
        (today,),
        default=0.0,
    )
    # Last health check: simplify to ok/error
    health_overall = "UNKNOWN"
    if _HEALTH_CHECK_AVAILABLE:
        try:
            results = HealthCheck.run_all()
            if isinstance(results, dict):
                statuses = [
                    v.get("ok", True) if isinstance(v, dict) else bool(v)
                    for v in results.values()
                ]
                health_overall = "OK" if all(statuses) else "DEGRADED"
        except Exception:  # noqa: BLE001
            health_overall = "ERROR"

    payload = {
        "system_state": "HALTED" if ks.get("active") else "RUNNING",
        "kill_switch": ks,
        "signals_1h": signals_1h,
        "trades_today": trades_today,
        "pnl_today": pnl_today,
        "active_lanes": active_lanes,
        "last_health_check": health_overall,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(payload)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GB-BRAIN Monitor Dashboard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--port", type=int, default=5001,
        help="TCP port to listen on (default: 5001)",
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Host / bind address (default: 127.0.0.1; use 0.0.0.0 for LAN)",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable Flask debug / hot-reload mode",
    )
    args = parser.parse_args()

    print(f"GB-BRAIN Monitor  →  http://{args.host}:{args.port}/")
    print(f"  DB path        : {DB_PATH}")
    print(f"  Kill switch    : {KILL_SWITCH_PATH}")
    print(f"  Debug mode     : {args.debug}")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
