import os
import time
import hashlib
import importlib.util
import requests

#  Load config
def load_config():
    spec = importlib.util.spec_from_file_location(
        "config",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_config.py"),
    )
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg


def load_secrets():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_secrets.py")
    spec = importlib.util.spec_from_file_location("secrets", p)
    sec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sec)
    return sec


cfg = load_config()
secrets = load_secrets()

GITHUB_TOKEN = secrets.GITHUB_TOKEN
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}
OUT_DIR = cfg.TRANSLATED_DIR
os.makedirs(OUT_DIR, exist_ok=True)

#  Search queries (broad coverage: elite, crypto, indices, indicators, ML, topics, niche)
QUERIES = [

    # ── ELITE ─────────────────────────────
    "trading strategy language:Python stars:>500",
    "algorithmic trading language:Python stars:>500",
    "quantitative trading language:Python stars:>500",
    "backtest trading strategy language:Python stars:>500",
    "trading strategy language:PineScript stars:>300",
    "systematic trading language:Python stars:>500",
    "high frequency trading language:Python stars:>300",

    # ── CRYPTO BEAST ──────────────────────
    "BTC ETH trading strategy language:PineScript stars:>50",
    "SOL XRP crypto strategy language:PineScript stars:>20",
    "crypto trading bot language:Python stars:>100",
    "crypto trading bot language:Python stars:>30",
    "futures crypto strategy language:Python stars:>30",
    "bitcoin trading strategy language:Python stars:>50",
    "ethereum defi strategy language:Python stars:>20",
    "crypto scalping strategy language:PineScript stars:>15",
    "crypto momentum strategy language:Python stars:>20",
    "DOGE SHIB meme coin trading language:PineScript stars:>10",
    "binance futures trading bot language:Python stars:>50",
    "bybit okx trading strategy language:Python stars:>20",
    "crypto grid trading bot language:Python stars:>20",
    "crypto arbitrage strategy language:Python stars:>30",

    # ── INDICES / CFD ─────────────────────
    "US30 NAS100 SPX500 trading strategy language:PineScript stars:>20",
    "SPX SPY index trading strategy language:Python stars:>30",
    "NAS100 NASDAQ trading strategy language:PineScript stars:>15",
    "Dow Jones US30 strategy language:PineScript stars:>10",
    "S&P500 futures strategy language:Python stars:>30",
    "index CFD swing trading language:PineScript stars:>10",
    "ES NQ futures trading system language:Python stars:>20",
    "stock index breakout strategy language:Python stars:>20",

    # ── INDICATOR COMBOS ──────────────────
    "EMA RSI MACD trading strategy language:PineScript stars:>20",
    "EMA RSI MACD trading strategy language:Python stars:>20",
    "VWAP trading strategy language:PineScript stars:>15",
    "Bollinger Bands RSI strategy language:PineScript stars:>15",
    "ATR trailing stop strategy language:PineScript stars:>10",
    "Stochastic RSI strategy language:PineScript stars:>10",
    "supertrend strategy language:PineScript stars:>15",
    "ichimoku cloud trading language:PineScript stars:>10",
    "MACD crossover strategy language:Python stars:>20",
    "moving average crossover strategy language:PineScript stars:>20",

    # ── STRATEGY TYPES ────────────────────
    "momentum trading strategy language:Python stars:>50",
    "mean reversion strategy language:Python stars:>30",
    "breakout trading strategy language:PineScript stars:>20",
    "scalping strategy language:PineScript stars:>20",
    "swing trading strategy language:PineScript stars:>20",
    "trend following strategy language:Python stars:>50",
    "pairs trading strategy language:Python stars:>30",
    "market making strategy language:Python stars:>30",
    "statistical arbitrage language:Python stars:>30",
    "overnight gap trading strategy language:PineScript stars:>10",
    "range trading strategy language:PineScript stars:>10",

    # ── MACHINE LEARNING ──────────────────
    "machine learning trading strategy language:Python stars:>100",
    "LSTM trading prediction language:Python stars:>50",
    "reinforcement learning trading language:Python stars:>50",
    "XGBoost trading strategy language:Python stars:>30",
    "neural network stock trading language:Python stars:>50",
    "deep learning crypto trading language:Python stars:>30",
    "transformer model trading signal language:Python stars:>20",
    "genetic algorithm trading strategy language:Python stars:>20",

    # ── TOPIC-TAGGED ──────────────────────
    "topic:pinescript topic:trading-strategy stars:>20",
    "topic:trading-bot topic:cryptocurrency stars:>30",
    "topic:backtesting topic:trading stars:>50 language:Python",
    "topic:quantitative-finance language:Python stars:>100",
    "topic:algorithmic-trading language:Python stars:>50",
    "topic:forex topic:trading language:Python stars:>20",
    "topic:crypto topic:strategy language:PineScript stars:>15",
    "topic:futures topic:trading language:Python stars:>20",
    "topic:trading topic:pine-script stars:>10",

    # ── NICHE GEM HUNTER ──────────────────
    "algorithmic trading crypto language:Python stars:>10",
    "backtest trading strategy language:Python stars:>10",
    "trading strategy language:PineScript stars:>5 pushed:>2024-01-01",
    "crypto bot strategy language:Python stars:>5 pushed:>2024-06-01",
    "NAS100 US30 strategy language:PineScript stars:>5",
    "trading signal indicator language:PineScript stars:>5 pushed:>2024-01-01",
    "futures scalping strategy language:Python stars:>5",
    "crypto trading script language:Python stars:>5 pushed:>2024-01-01",
    "pine script strategy backtest stars:>5 pushed:>2024-03-01",

    # ── FRAMEWORK / ENGINE ────────────────
    "freqtrade strategy language:Python stars:>20",
    "backtrader strategy language:Python stars:>20",
    "jesse trading strategy language:Python stars:>10",
    "zipline trading strategy language:Python stars:>20",
    "vectorbt strategy language:Python stars:>20",
    "nautilus trader strategy language:Python stars:>20",
    "hummingbot strategy language:Python stars:>20",
]

CRYPTO_KEYWORDS = [
    "btc",
    "eth",
    "sol",
    "crypto",
    "usdt",
    "binance",
    "bybit",
    "blofin",
    "bitcoin",
    "ethereum",
    "solana",
    "futures",
    "perpetual",
    "us30",
    "nas100",
    "spx500",
    "spx",
    "spy",
    "es",
    "nq",
    "dow jones",
    "s&p500",
]

STRATEGY_KEYWORDS = [
    "strategy",
    "signal",
    "entry",
    "exit",
    "backtest",
    "win_rate",
    "winrate",
    "long",
    "short",
    "ema",
    "rsi",
    "macd",
    "bollinger",
]

downloaded = set()
stats = {"repos_found": 0, "files_downloaded": 0, "skipped": 0}


def handle_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", "99"))
    reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
    if remaining < 5 and reset_time > 0:
        wait = max(reset_time - time.time(), 0) + 2
        print(f"  Rate limit low ({remaining} left) — sleeping {wait:.0f}s")
        time.sleep(wait)


def search_repos(query, page=1):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 30,
        "page": page,
    }
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    if r.status_code == 200:
        handle_rate_limit(r)
        return r.json().get("items", [])
    if r.status_code == 403:
        handle_rate_limit(r)
    return []


def get_repo_files(owner, repo, path="", depth=0):
    if depth > 3:
        return []
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException:
        return []
    if r.status_code != 200:
        return []
    files = []
    for item in r.json():
        if item["type"] == "file":
            name = item["name"].lower()
            if name.endswith(".py") or name.endswith(".pine"):
                files.append(item)
        elif item["type"] == "dir" and depth < 2:
            subdir = item["name"].lower()
            if any(k in subdir for k in ["strat", "signal", "trade", "bot", "algo", "backtest", "script"]):
                files.extend(get_repo_files(owner, repo, item["path"], depth + 1))
    return files


def is_relevant(content_str, ext):
    if ext == ".pine":
        return True
    low = content_str.lower()
    has_market = any(k in low for k in CRYPTO_KEYWORDS)
    strategy_hits = sum(1 for k in STRATEGY_KEYWORDS if k in low)
    return strategy_hits >= 4 or (has_market and strategy_hits >= 2)


def download_file(item, repo_name, owner, stars, retries=2):
    ext = ".pine" if item["name"].lower().endswith(".pine") else ".py"
    base_key = f"{owner}_{repo_name}_{item['name']}_{stars}"
    hash_suffix = hashlib.sha1(base_key.encode("utf-8")).hexdigest()[:8]
    fname_key = f"{owner}_{repo_name}_{item['name']}_{hash_suffix}"

    if fname_key in downloaded:
        stats["skipped"] += 1
        return

    content = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(item["download_url"], headers=HEADERS, timeout=15)
            if r.status_code == 200:
                content = r.text
                break
            if attempt < retries:
                time.sleep(2 ** attempt)
        except requests.RequestException:
            if attempt < retries:
                time.sleep(2)
            else:
                return
    if content is None:
        return

    if not is_relevant(content, ext):
        stats["skipped"] += 1
        return

    safe_name = fname_key.replace("/", "_").replace(" ", "_")[:120]
    out_path = os.path.join(OUT_DIR, safe_name if safe_name.endswith(ext) else safe_name + ext)
    with open(out_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(f"# SOURCE: https://github.com/{owner}/{repo_name}\n")
        f.write(f"# FILE  : {item['name']}\n\n")
        f.write(content)
    downloaded.add(fname_key)
    stats["files_downloaded"] += 1
    print(f"  SAVED: {safe_name[:80]}")


print("=" * 60)
print("PHANTOMFLIP STRATEGY HARVESTER")
print(f"Output: {OUT_DIR}")
print("=" * 60)

seen_repos = set()
for query in QUERIES:
    print(f"\nSearching: {query[:80]}")
    for page in [1, 2]:
        repos = search_repos(query, page)
        for repo in repos:
            key = repo["full_name"]
            if key in seen_repos:
                continue
            seen_repos.add(key)
            stats["repos_found"] += 1
            owner, rname = repo["owner"]["login"], repo["name"]
            stars = repo["stargazers_count"]
            print(f"  [{stars}*] {key}")
            files = get_repo_files(owner, rname)
            for f in files:
                download_file(f, rname, owner, stars)
                time.sleep(0.3)
        time.sleep(2)
    print(
        f"\n  Progress: {len(seen_repos)} repos | "
        f"{stats['files_downloaded']} saved | {stats['skipped']} skipped"
    )
    time.sleep(3)

print("\n" + "=" * 60)
print("DONE!")
print(f"  Repos scanned   : {stats['repos_found']}")
print(f"  Files downloaded: {stats['files_downloaded']}")
print(f"  Skipped (low relevance): {stats['skipped']}")
print("\nNext step: run python 1_clone_translate.py")
print("=" * 60)
