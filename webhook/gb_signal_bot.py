import json, logging, os, sqlite3, sys
from datetime import datetime, timezone, date
from pathlib import Path
from flask import Flask, request, jsonify
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dotenv import load_dotenv
load_dotenv(ROOT / '.env')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT  = os.getenv('TELEGRAM_CHAT_ID')
WEBHOOK_SECRET = os.getenv('GB_SIGNAL_SECRET', 'gbsignal2026')
PORT           = int(os.getenv('GB_SIGNAL_PORT', '5001'))
DB_PATH        = ROOT / 'db' / 'gb_brain.db'
LOG_DIR        = ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# ATR filter — skip signal if ATR is below this (dead/choppy market)
# US30 typical ATR on 15m is 80-200pts. Below 50 = too quiet to trade.
ATR_MIN_US30   = float(os.getenv('ATR_MIN_US30', '50'))

# RR ratio for TP calculation
RR_TARGET      = float(os.getenv('RR_TARGET', '2.0'))

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('/var/log/gb-brain/gb_signal_bot.log'), logging.StreamHandler()])
logger = logging.getLogger('gb_signal_bot')
app = Flask(__name__)

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT: return
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)
    except Exception as e: logger.warning(f'Telegram: {e}')

def get_session_label():
    now = datetime.now(timezone.utc); h = now.hour; m = now.minute
    if h == 13 and 25 <= m <= 35: return 'NY_ORB'
    elif 13 <= h < 20: return 'NY'
    elif 8 <= h < 13: return 'LONDON'
    elif 0 <= h < 8: return 'ASIA'
    return 'OFF'

def in_session():
    now = datetime.now(timezone.utc); mins = now.hour*60+now.minute
    return (12*60+30) <= mins <= (16*60+30)

def calc_sl_tp(data):
    """
    Calculate SL and TP from signal data.
    Priority: use ATR if provided, else use candle high/low.
    Returns: sl, tp, sl_pts, tp_pts, rr
    """
    action = data.get('action','').upper()
    price  = float(data.get('price', 0) or 0)
    high   = float(data.get('high',  price) or price)
    low    = float(data.get('low',   price) or price)
    atr    = float(data.get('atr',   0) or 0)

    if price == 0:
        return None, None, None, None, None

    direction = 'LONG' if action in ('BUY','LONG') else 'SHORT'

    if atr > 0:
        # ATR-based: SL = 1.0x ATR, TP = 2.0x ATR
        sl_dist = round(atr * 1.0)
        tp_dist = round(atr * RR_TARGET)
    else:
        # Candle-based: SL = beyond candle H/L, TP = 2x that distance
        if direction == 'LONG':
            sl_dist = round(price - low + 10)   # 10pt buffer below candle low
        else:
            sl_dist = round(high - price + 10)  # 10pt buffer above candle high
        tp_dist = round(sl_dist * RR_TARGET)

    if direction == 'LONG':
        sl = round(price - sl_dist)
        tp = round(price + tp_dist)
    else:
        sl = round(price + sl_dist)
        tp = round(price - tp_dist)

    rr = round(tp_dist / sl_dist, 1) if sl_dist > 0 else 0
    return sl, tp, sl_dist, tp_dist, rr

def check_atr_filter(data):
    """Returns (passed, reason)"""
    atr = float(data.get('atr', 0) or 0)
    symbol = data.get('symbol', '').upper()
    if atr == 0:
        return True, None   # No ATR in payload — pass (old alert format)
    if 'US30' in symbol or 'US30USD' in symbol:
        if atr < ATR_MIN_US30:
            return False, f'ATR {atr:.0f} < min {ATR_MIN_US30:.0f} (choppy market)'
    return True, None

def log_to_db(data, ctx, sl=None, tp=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        ex = {r[1] for r in conn.execute('PRAGMA table_info(live_trades);')}
        for col,typ in [('signal_price','REAL'),('source','TEXT'),('run_at','TEXT'),
                        ('raw_signal','TEXT'),('side','TEXT'),('strategy','TEXT'),
                        ('stop_loss','REAL'),('tp1','REAL')]:
            if col not in ex: conn.execute(f'ALTER TABLE live_trades ADD COLUMN {col} {typ};')
        conn.execute(
            'INSERT INTO live_trades (run_at,broker,symbol,timeframe,strategy,side,signal_price,stop_loss,tp1,source,raw_signal) '
            'VALUES (?,?,?,?,?,?,?,?,?,\"tv_signal\",?)',
            (datetime.utcnow().isoformat(), data.get('broker','tradingview'),
             data.get('symbol','?'), data.get('tf','15m'),
             data.get('signal','PARALLAX'), data.get('action','?').upper(),
             data.get('price'), sl, tp, json.dumps({**data,**ctx})))
        conn.commit(); conn.close()
    except Exception as e: logger.error(f'DB: {e}')

def log_to_file(data, ctx):
    with open(LOG_DIR/'session_log.jsonl','a') as f:
        f.write(json.dumps({'timestamp':datetime.utcnow().isoformat(),'data':data,'context':ctx})+'\n')

@app.route('/health')
def health():
    return jsonify({'status':'ok','session':get_session_label(),'in_session':in_session()})

@app.route('/signal', methods=['POST'])
def receive_signal():
    try:
        data = request.get_json(force=True, silent=True) or {}
        if data.get('secret') != WEBHOOK_SECRET:
            return jsonify({'error':'unauthorized'}), 401

        ctx = {
            'received_at':   datetime.utcnow().isoformat(),
            'in_session':    in_session(),
            'session_label': get_session_label()
        }

        # ATR filter
        atr_ok, atr_reason = check_atr_filter(data)
        if not atr_ok:
            logger.info(f'Signal FILTERED — {atr_reason}')
            ctx['filtered'] = True
            ctx['filter_reason'] = atr_reason
            log_to_file(data, ctx)
            send_telegram(
                f'<b>⚡ {data.get("signal","SIGNAL")} — ⚠️ FILTERED</b>\n'
                f'Symbol : {data.get("symbol","?")}\n'
                f'Reason : {atr_reason}\n'
                f'<i>Signal skipped — choppy market</i>'
            )
            return jsonify({'status':'filtered','reason':atr_reason}), 200

        # Calculate SL/TP
        sl, tp, sl_pts, tp_pts, rr = calc_sl_tp(data)

        log_to_db(data, ctx, sl=sl, tp=tp)
        log_to_file(data, ctx)

        action    = data.get('action','?').upper()
        direction = 'LONG' if action in ('BUY','LONG') else 'SHORT'
        emoji     = '🟢' if direction == 'LONG' else '🔴'
        orb_tag   = ' 🎯 ORB' if ctx['session_label'] == 'NY_ORB' else ''
        sess_tag  = '✅ IN SESSION' if ctx['in_session'] else '⚠️ OUTSIDE SESSION'

        # ORB levels from payload (if sent)
        orb_h = data.get('orb_high')
        orb_l = data.get('orb_low')
        atr   = data.get('atr')

        orb_line = ''
        if orb_h and orb_l:
            orb_line = f'ORB    : H {orb_h} / L {orb_l}\n'

        atr_line = f'ATR    : {float(atr):.0f} pts\n' if atr else ''

        sl_line = ''
        if sl and tp and sl_pts and tp_pts:
            sl_line = (
                f'──────────────────\n'
                f'SL     : <b>{sl}</b>  ({sl_pts} pts)\n'
                f'TP     : <b>{tp}</b>  ({tp_pts} pts)\n'
                f'RR     : 1:{rr}\n'
            )

        msg = (
            f'<b>⚡ {data.get("signal","SIGNAL")} — {emoji} {direction}</b>\n'
            f'Symbol : <b>{data.get("symbol","?")}</b>\n'
            f'Price  : <b>{data.get("price","?")}</b>\n'
            f'H/L    : {data.get("high","?")} / {data.get("low","?")}\n'
            f'{atr_line}'
            f'{orb_line}'
            f'{sl_line}'
            f'Session: {ctx["session_label"]}{orb_tag}\n'
            f'{sess_tag}'
        )

        send_telegram(msg)
        logger.info(f'Signal: {data.get("signal")} {action} {data.get("symbol")} @ {data.get("price")} | SL:{sl} TP:{tp} RR:1:{rr}')
        return jsonify({'status':'logged','session':ctx['session_label']}), 200

    except Exception as e:
        logger.error(f'Error: {e}'); return jsonify({'error':str(e)}), 500

@app.route('/session/summary')
def summary():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        'SELECT side,symbol,signal_price,strategy,run_at,stop_loss,tp1 FROM live_trades '
        'WHERE source="tv_signal" AND run_at>=? ORDER BY run_at DESC',
        (date.today().isoformat(),)).fetchall()
    conn.close()
    return jsonify({'total':len(rows),'signals':[
        {'side':r[0],'symbol':r[1],'price':r[2],'strategy':r[3],'time':r[4],'sl':r[5],'tp':r[6]}
        for r in rows]})

if __name__ == '__main__':
    logger.info(f'GB-SIGNAL Bot v2 on port {PORT}')
    send_telegram(f'<b>🤖 GB-SIGNAL Bot v2 ONLINE</b>\nATR filter: {ATR_MIN_US30:.0f}pt min\nRR target: 1:{RR_TARGET}\nSession: 6:30-10:30am MDT')
    app.run(host='0.0.0.0', port=PORT, debug=False)
