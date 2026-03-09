> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(20 Jan 1990 00:00 +0900)|(?Time)Start Date|
|v_input_2|timestamp(20 Dec 2030 00:00 +0900)|End Date|
|v_input_string_1|0|(?Strategy: Stop Loss Conditions)SL Type : ATR|Percent|Previous LL / HH|
|v_input_float_1|3|SL % |
|v_input_int_1|14|SL ATR Length |
|v_input_float_2|4|SL ATR Multiplier|
|v_input_int_2|30|Lowest Price Before Entry|
|v_input_float_3|2|(?Strategy: Risk Management)Risk : Reward Ratio |
|v_input_float_4|true|Portfolio Risk %|
|v_input_bool_1|false|(?Strategy: Drawings)Show TP / SL Boxes|
|v_input_bool_2|false|Show Trade Exit Labels|
|v_input_bool_3|false|Show Dashboard|
|v_input_bool_4|false|Color Bars|
|v_input_bool_5|true|(?1: SSL Hybrid)use true range for Keltner Channel?|
|v_input_string_2|0|Baseline Type: EMA|SMA|DEMA|TEMA|LSMA|WMA|MF|VAMA|TMA|HMA|JMA|Kijun v2|EDSMA|McGinley|
|v_input_int_3|30|Baseline Length|
|v_input_float_5|0.2|Base Channel Multiplier|
|v_input_int_4|true|Kijun MOD Divider|
|v_input_int_5|3|Baseline Type = JMA -> Jurik Phase|
|v_input_int_6|true|Baseline Type = JMA -> Jurik Power|
|v_input_int_7|10|Baseline Type = VAMA -> Volatility lookback length|
|v_input_float_6|0.8|Baseline Type = MF (Modular Filter, General Filter) ->Beta|
|v_input_bool_6|false|Baseline Type = MF (Modular Filter) -> Use Feedback?|
|v_input_float_7|0.5|Baseline Type = MF (Modular Filter) -> Feedback Weighting|
|v_input_int_8|20|EDSMA - Super Smoother Filter Length|
|v_input_int_9|0|EDSMA - Super Smoother Filter Poles: 2|3|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// Thanks to @kevinmck100 for opensource strategy template and @Mihkel00 for SSL Hybrid
// @fpemehd
// @version=5
strategy(title = '[fpemehd] SSL Baseline Strategy',
         shorttitle = '[f] SSL',
         overlay = true)

// # ========================================================================= #
// #                                Inputs 
// # ========================================================================= #

// 1. Time
i_start                 = input (defval = timestamp("20 Jan 1990 00:00 +0900"), title = "Start Date", tooltip = "Choose Backtest Start Date", inline=false)
i_end                   = input (defval = timestamp("20 Dec 2030 00:00 +0900"), title = "End Date", tooltip = "Choose Backtest End Date")
i_sl_type               = input ("ATR", title = "SL Type : ATR|Percent|Previous LL / HH", tooltip = "Select Stop Loss Type")
i_sl_percentage         = input(3.0, title="SL %", type=input.float)
i_sl_atr_length         = input(14, title="SL ATR Length", type=input.integer)
i_sl_atr_multiplier     = input(4.0, title="SL ATR Multiplier", type=input.float)
i_entry_lowest_price    = input(30, title="Lowest Price Before Entry", type=input.integer)
i_risk_reward_ratio     = input(2.0, title="Risk : Reward Ratio", type=input.float)
i_portfolio_risk        = input(true, title="Portfolio Risk %")
i_show_tp_sl_boxes      = input(false, title="Show TP / SL Boxes")
i_show_trade_exit_labels= input(false, title="Show Trade Exit Labels")
i_show_dashboard        = input(false, title="Show Dashboard")
i_color_bars            = input(false, title="Color Bars")
i_ssl_hybrid_use_true_range = input(true, title="(?1: SSL Hybrid)use true range for Keltner Channel?")
i_baseline_type         = input("EMA", title="Baseline Type: EMA|SMA|DEMA|TEMA|LSMA|WMA|MF|VAMA|TMA|HMA|JMA|Kijun v2|EDSMA|McGinley")
i_baseline_length       = input(30, title="Baseline Length", type=input.integer)
i_base_channel_multiplier= input(0.2, title="Base Channel Multiplier", type=input.float)
i_kijun_mod_divider     = input(true, title="Kijun MOD Divider")
i_jurik_phase           = input(3, title="Baseline Type = JMA -> Jurik Phase", type=input.integer)
i_jurik_power           = input(true, title="Baseline Type = JMA -> Jurik Power")
i_vama_volatility_lookback= input(10, title="Baseline Type = VAMA -> Volatility lookback length", type=input.integer)
i_mf_beta               = input(0.8, title="Baseline Type = MF (Modular Filter, General Filter) ->Beta", type=input.float)
i_mf_feedback           = input(false, title="Baseline Type = MF (Modular Filter) -> Use Feedback?")
i_mf_feedback_weighting  = input(0.5, title="Baseline Type = MF (Modular Filter) -> Feedback Weighting", type=input.float)
i_edsma_length          = input(20, title="EDSMA - Super Smoother Filter Length", type=input.integer)
i_edsma_poles           = input(0, title="EDSMA - Super Smoother Filter Poles: 2|3", type=input.integer)
```