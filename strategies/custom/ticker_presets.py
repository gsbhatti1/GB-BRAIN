"""
GB-BRAIN — Ticker Presets
===========================
Per-ticker optimized settings for Cipher, Parallax, and Combined strategies.
Based on: GEM analysis (591 SPX, 18 SOL, 2 ETH), live trading observations,
and institutional behavior patterns.

Usage:
    from strategies.custom.ticker_presets import get_preset
    preset = get_preset("US30", "5m")
"""

PRESETS = {
    # ═══════════════════════════════════════════════
    # US30 (Dow Jones Industrial Average)
    # ═══════════════════════════════════════════════
    "US30": {
        "display_name": "US30 (Dow Jones)",
        "yahoo_symbol": "^DJI",
        "binance_symbol": None,
        "round_increment": 250,
        "best_timeframes": ["5m", "15m"],

        "parallax": {
            "orb_window_minutes": 5,           # 09:25-09:30 ET
            "confirm_candles": 2,
            "min_target_pts": 100,             # US30 moves 100-300 pts
            "swing_sl_bars": 6,
            "rsi_safe_lo": 20,
            "rsi_safe_hi": 80,
            "max_or_range": 150,               # Reject if ORB > 150 pts
            "min_or_range": 10,                # Reject if ORB < 10 pts
            "session_ny": True,
            "session_london": False,           # Low conviction for US indices
            "session_asia": False,             # Very low conviction
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.40,
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 5,
            "entry_cooldown_bars": 2,
            "choch_entry_window": 15,
            "min_target_pts": 100,
            "swing_sl_bars": 6,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.40,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,              # Test with True for higher WR
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 65,             # Score 0-100, enter above this
            "weights": {
                "choch_active": 20,
                "fvg_golden": 15,
                "ob_proximity": 10,
                "ote_zone": 10,
                "premium_discount": 5,
                "parallax_trap": 20,
                "parallax_confirm": 10,
                "rsi_safe": 5,
                "bollinger_position": 5,
                "volume_above_avg": 5,
                "no_news_window": 5,
                "not_monday": 3,
                "round_level_proximity": 7,
            },
        },

        # Kill zones (ET)
        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 1.0},
            {"name": "NY_LUNCH", "start": "11:30", "end": "13:30", "weight": 0.3},
            {"name": "NY_PM", "start": "14:00", "end": "15:30", "weight": 0.6},
        ],

        # News blackout windows (ET)
        "news_windows": [
            {"start": "08:25", "end": "08:40"},   # NFP, CPI, PPI
            {"start": "09:55", "end": "10:10"},   # ISM
            {"start": "13:55", "end": "14:45"},   # FOMC
        ],
    },

    # ═══════════════════════════════════════════════
    # NAS100 (Nasdaq 100)
    # ═══════════════════════════════════════════════
    "NAS100": {
        "display_name": "NAS100 (Nasdaq)",
        "yahoo_symbol": "^NDX",
        "binance_symbol": None,
        "round_increment": 500,
        "best_timeframes": ["5m", "15m"],

        "parallax": {
            "orb_window_minutes": 5,
            "confirm_candles": 2,
            "min_target_pts": 150,             # NAS moves bigger
            "swing_sl_bars": 6,
            "rsi_safe_lo": 20,
            "rsi_safe_hi": 80,
            "max_or_range": 250,
            "min_or_range": 15,
            "session_ny": True,
            "session_london": False,
            "session_asia": False,
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 5,
            "entry_cooldown_bars": 2,
            "choch_entry_window": 15,
            "min_target_pts": 150,
            "swing_sl_bars": 6,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 65,
            "weights": {
                "choch_active": 20,
                "fvg_golden": 15,
                "ob_proximity": 10,
                "ote_zone": 10,
                "premium_discount": 5,
                "parallax_trap": 20,
                "parallax_confirm": 10,
                "rsi_safe": 5,
                "bollinger_position": 5,
                "volume_above_avg": 5,
                "no_news_window": 5,
                "not_monday": 3,
                "round_level_proximity": 7,
            },
        },

        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 1.0},
            {"name": "NY_LUNCH", "start": "11:30", "end": "13:30", "weight": 0.3},
            {"name": "NY_PM", "start": "14:00", "end": "15:30", "weight": 0.6},
        ],

        "news_windows": [
            {"start": "08:25", "end": "08:40"},
            {"start": "09:55", "end": "10:10"},
            {"start": "13:55", "end": "14:45"},
        ],
    },

    # ═══════════════════════════════════════════════
    # SPX500 (S&P 500)
    # ═══════════════════════════════════════════════
    "SPX500": {
        "display_name": "SPX500 (S&P 500)",
        "yahoo_symbol": "^GSPC",
        "binance_symbol": None,
        "round_increment": 50,
        "best_timeframes": ["15m", "30m"],

        "parallax": {
            "orb_window_minutes": 5,
            "confirm_candles": 2,
            "min_target_pts": 30,              # SPX smaller moves
            "swing_sl_bars": 6,
            "rsi_safe_lo": 25,
            "rsi_safe_hi": 75,
            "max_or_range": 30,
            "min_or_range": 3,
            "session_ny": True,
            "session_london": False,
            "session_asia": False,
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.40,
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 5,
            "entry_cooldown_bars": 2,
            "choch_entry_window": 12,
            "min_target_pts": 30,
            "swing_sl_bars": 6,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.40,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 70,             # Higher threshold — SPX is less volatile
            "weights": {
                "choch_active": 20,
                "fvg_golden": 15,
                "ob_proximity": 10,
                "ote_zone": 10,
                "premium_discount": 5,
                "parallax_trap": 20,
                "parallax_confirm": 10,
                "rsi_safe": 5,
                "bollinger_position": 5,
                "volume_above_avg": 5,
                "no_news_window": 5,
                "not_monday": 3,
                "round_level_proximity": 7,
            },
        },

        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 1.0},
            {"name": "NY_PM", "start": "14:00", "end": "15:30", "weight": 0.6},
        ],

        "news_windows": [
            {"start": "08:25", "end": "08:40"},
            {"start": "09:55", "end": "10:10"},
            {"start": "13:55", "end": "14:45"},
        ],
    },

    # ═══════════════════════════════════════════════
    # BTC (Bitcoin)
    # ═══════════════════════════════════════════════
    "BTC": {
        "display_name": "BTC (Bitcoin)",
        "yahoo_symbol": "BTC-USD",
        "binance_symbol": "BTCUSDT",
        "round_increment": 1000,
        "best_timeframes": ["15m", "1h"],

        "parallax": {
            "orb_window_minutes": 15,          # Wider ORB for 24/7 market
            "confirm_candles": 3,              # More confirms for crypto volatility
            "min_target_pts": 500,             # BTC moves in $100s-$1000s
            "swing_sl_bars": 6,
            "rsi_safe_lo": 25,
            "rsi_safe_hi": 75,
            "max_or_range": 2000,
            "min_or_range": 100,
            "session_ny": True,                # NY session has most BTC volume
            "session_london": True,            # London also significant for BTC
            "session_asia": True,              # Asia is real for crypto
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 7,               # Wider swing for BTC noise
            "entry_cooldown_bars": 3,
            "choch_entry_window": 20,          # Longer window for BTC
            "min_target_pts": 500,
            "swing_sl_bars": 8,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 60,             # Lower threshold — more opportunity in crypto
            "weights": {
                "choch_active": 20,
                "fvg_golden": 15,
                "ob_proximity": 10,
                "ote_zone": 10,
                "premium_discount": 5,
                "parallax_trap": 18,
                "parallax_confirm": 10,
                "rsi_safe": 5,
                "bollinger_position": 7,       # BB works great for BTC
                "volume_above_avg": 8,
                "no_news_window": 2,           # Less news impact on crypto
                "not_monday": 0,               # No day bias in crypto
                "round_level_proximity": 5,
            },
        },

        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 0.9},
            {"name": "LONDON", "start": "03:00", "end": "05:00", "weight": 0.7},
            {"name": "ASIA", "start": "20:00", "end": "23:00", "weight": 0.5},
        ],

        "news_windows": [
            {"start": "13:55", "end": "14:45"},   # FOMC still moves BTC
        ],
    },

    # ═══════════════════════════════════════════════
    # ETH (Ethereum)
    # ═══════════════════════════════════════════════
    "ETH": {
        "display_name": "ETH (Ethereum)",
        "yahoo_symbol": "ETH-USD",
        "binance_symbol": "ETHUSDT",
        "round_increment": 100,
        "best_timeframes": ["15m", "1h"],

        "parallax": {
            "orb_window_minutes": 15,
            "confirm_candles": 3,
            "min_target_pts": 50,
            "swing_sl_bars": 6,
            "rsi_safe_lo": 25,
            "rsi_safe_hi": 75,
            "max_or_range": 200,
            "min_or_range": 10,
            "session_ny": True,
            "session_london": True,
            "session_asia": True,
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 7,
            "entry_cooldown_bars": 3,
            "choch_entry_window": 20,
            "min_target_pts": 50,
            "swing_sl_bars": 8,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.35,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 60,
            "weights": {
                "choch_active": 20,
                "fvg_golden": 15,
                "ob_proximity": 10,
                "ote_zone": 10,
                "premium_discount": 5,
                "parallax_trap": 18,
                "parallax_confirm": 10,
                "rsi_safe": 5,
                "bollinger_position": 7,
                "volume_above_avg": 8,
                "no_news_window": 2,
                "not_monday": 0,
                "round_level_proximity": 5,
            },
        },

        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 0.9},
            {"name": "LONDON", "start": "03:00", "end": "05:00", "weight": 0.7},
            {"name": "ASIA", "start": "20:00", "end": "23:00", "weight": 0.5},
        ],

        "news_windows": [
            {"start": "13:55", "end": "14:45"},
        ],
    },

    # ═══════════════════════════════════════════════
    # SOL (Solana) — YOUR GOLDEN CHARM
    # ═══════════════════════════════════════════════
    "SOL": {
        "display_name": "SOL (Solana) ★",
        "yahoo_symbol": "SOL-USD",
        "binance_symbol": "SOLUSDT",
        "round_increment": 5,
        "best_timeframes": ["5m", "15m"],

        "parallax": {
            "orb_window_minutes": 10,          # Tighter for SOL speed
            "confirm_candles": 2,              # SOL moves fast
            "min_target_pts": 2.0,             # SOL in dollars
            "swing_sl_bars": 5,
            "rsi_safe_lo": 25,
            "rsi_safe_hi": 75,
            "max_or_range": 10,
            "min_or_range": 0.5,
            "session_ny": True,
            "session_london": True,
            "session_asia": True,
            "ny_open": "09:30",
            "ny_close": "16:00",
            "trail_pct": 0.30,                 # Tighter trail for SOL volatility
            "breakeven_at_1r": True,
        },

        "cipher": {
            "swing_lookback": 5,
            "entry_cooldown_bars": 2,
            "choch_entry_window": 12,
            "min_target_pts": 2.0,
            "swing_sl_bars": 5,
            "ote_low": 0.62,
            "ote_high": 0.79,
            "ote_sweet": 0.705,
            "trail_pct": 0.30,
            "breakeven_at_1r": True,
            "require_choch": True,
            "require_fvg": False,
            "require_ote": False,
            "require_discount": False,
            "require_trend_agree": True,
            "require_swing_valid": True,
            "require_break_swing": True,
        },

        "combined": {
            "entry_threshold": 55,             # Lower — SOL has proven high WR
            "weights": {
                "choch_active": 18,
                "fvg_golden": 12,
                "ob_proximity": 8,
                "ote_zone": 8,
                "premium_discount": 5,
                "parallax_trap": 18,
                "parallax_confirm": 10,
                "rsi_safe": 8,                 # RSI is king for SOL (10/18 GEMs)
                "bollinger_position": 8,
                "volume_above_avg": 10,        # Volume matters more for SOL
                "no_news_window": 2,
                "not_monday": 0,
                "round_level_proximity": 3,
            },
        },

        # SOL-specific: Add Chande Momentum Oscillator (89.9% WR in GEMs)
        "special_indicators": {
            "cmo_period": 9,
            "cmo_oversold": -50,               # Buy when CMO < -50
            "cmo_overbought": 50,              # Sell when CMO > 50
            "use_cmo": True,
        },

        "kill_zones": [
            {"name": "NY_OPEN", "start": "09:30", "end": "11:00", "weight": 0.8},
            {"name": "LONDON", "start": "03:00", "end": "05:00", "weight": 0.7},
            {"name": "ASIA", "start": "20:00", "end": "23:00", "weight": 0.6},
        ],

        "news_windows": [],  # Crypto less affected by US economic data
    },
}

# Alias mapping
TICKER_ALIASES = {
    "^DJI": "US30", "DJI": "US30", "YM": "US30", "DJIA": "US30",
    "^NDX": "NAS100", "NDX": "NAS100", "NQ": "NAS100", "NASDAQ": "NAS100",
    "^GSPC": "SPX500", "GSPC": "SPX500", "ES": "SPX500", "SPX": "SPX500", "SP500": "SPX500",
    "BTCUSDT": "BTC", "BTC-USD": "BTC", "BITCOIN": "BTC", "XBT": "BTC",
    "ETHUSDT": "ETH", "ETH-USD": "ETH", "ETHEREUM": "ETH",
    "SOLUSDT": "SOL", "SOL-USD": "SOL", "SOLANA": "SOL",
}


def get_preset(ticker, timeframe=None):
    """Get preset for a ticker. Resolves aliases."""
    key = TICKER_ALIASES.get(ticker.upper(), ticker.upper())
    if key not in PRESETS:
        raise ValueError(f"Unknown ticker: {ticker}. Available: {list(PRESETS.keys())}")
    preset = PRESETS[key].copy()
    if timeframe:
        preset["active_timeframe"] = timeframe
    return preset


def list_tickers():
    """List all available tickers with their display names."""
    return {k: v["display_name"] for k, v in PRESETS.items()}
