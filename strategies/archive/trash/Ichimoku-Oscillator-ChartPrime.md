> Name

Ichimoku-Oscillator-ChartPrime-Indicator

> Author

Mirror Water Moon


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_source_1_close|0|(?Settings)Signal Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_1|9|Conversion Line Length|
|v_input_int_2|26|Base Line Length|
|v_input_int_3|52|Leading Span B Length|
|v_input_int_4|26|Lagging Span|
|v_input_int_5|12|Moving Average Length|
|v_input_int_6|3|(?Smoothing)Smoothing|
|v_input_bool_1|true|extra_smoothing|
|v_input_string_1|Window|(?Normalization)Normalize|
|v_input_int_7|20|window_size|
|v_input_bool_2|true|Clamp to Range|
|v_input_float_1|2|Max Bandwidth|
|v_input_float_2|1.5|Mid Bandwidth|
|v_input_int_8|10|(?Divergence)Divergence Look Right|
|v_input_int_9|15|Divergence Look Left|
|v_input_int_10|100|Maximum Lookback|
|v_input_int_11|5|Minimum Lookback|
|v_input_string_2|Symbol|Show Labels|
|v_input_bool_3|true|Regular Bullish|
|v_input_bool_4|false|Hidden Bullish|
|v_input_bool_5|true|Regular Bearish|
|v_input_bool_6|false|Hidden Bearish|
|v_input_bool_7|true|(?Visibility)Show Signal|
|v_input_bool_8|false|Show Chikou|
|v_input_bool_9|false|Show Conversion and Base|
|v_input_bool_10|false|Show Moving Average|
|v_input_bool_11|true|Show Min/Max|
|v_input_string_3|Full|Show Kumo|
|v_input_bool_12|false|Show Kumbo Lines|
|v_input_bool_13|true|(?Color)Color Signal by Conversion Cross|
|v_input_color_1|#F36B16|Signal Color|
|v_input_int_12|2|signal_width|
|v_input_color_2|#22EA70|Kumo Color|
|v_input_color_3|#FF2F1C|kumo_bearish_color|
|v_input_int_13|10|v_input_int_13|
|v_input_color_4|gray|Chikou Color|
|v_input_color_5|#79D8E0|Conversion/Base Color|
|v_input_color_6|#E462B2|base_color|
|v_input_color_7|#1c7a24|Bullish CB Color|
|v_input_color_8|#64a568|base_color_bullish|
|v_input_color_9|#df8c8c|Bearish CB Color|
|v_input_color_10|#ff4444|base_color_bearish|
|v_input_color_11|#F2DB2E|Neutral Color|
|v_input_int_14|10|v_input_int_14|
|v_input_color_12|#5398ff|Moving Average Color|
|v_input_color_13|#5C9970|Top Colors|
|v_input_color_14|#32533D|high_color|
|v_input_int_15|10|v_input_int_15|
|v_input_color_15|#DD6055|Bottom Colors|
|v_input_color_16|#CF3729|low_color|
|v_input_int_16|10|v_input_int_16|
|v_input_color_17|#111122|Text Color|
|v_input_color_18|#46c47a|Bullish Colors|
|v_input_color_19|#802ac7|hidden_bullish_color|
|v_input_color_20|#f82e2e|Bearish Colors|
|v_input_color_21|#3176f5|hidden_bearish_color|


> Source (PineScript)

``` pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ChartPrime

//@version=5
indicator("Ichimoku Oscillator [ChartPrime]", max_lines_count = 500, max_labels_count = 500)

source = input.source(close, "Signal Source", group = "Settings")
conversion_periods = input.int(9, "Conversion Line Length", minval = 1, group = "Settings")
base_periods = input.int(26, "Base Line Length", minval = 1, group = "Settings")
lagging_span_periods = input.int(52, "Leading Span B Length", minval = 1, group = "Settings")
displacement = input.int(26, "Lagging Span", minval = 1, group = "Settings")
ma_length = input.int(12, "Moving Average Length", minval = 1, group = "Settings")

smoothing_length = input.int(3, "Smoothing", minval = 1, inline = "signal smoothing", group = "Smoothing")
extra_smoothing = input.bool(true, "", inline = "signal smoothing", tooltip = "Enable for extra smoothing.", group = "Smoothing")

normalize = input.string("Window", "Normalize", ["All", "Window", "Disabled"], group = "Normalization", inline = "Normalize")
window_size = input.int(20, "", minval = 5, tooltip = "When enabled it will scale from 100 to -100. If Normalize is set to 'All' it will take into account the whole series. If its set to 'Window', it use a window of data to normalize.", group = "Normalization", inline = "Normalize")
clamp = input.bool(true, "Clamp to Range", group = "Normalization")
top_band = input.float(2, "Max Bandwidth", minval = 0, step = 0.25, group = "Normalization")
mid_band = input.float(1.5, "Mid Bandwidth", minval = 0, step = 0.25, group = "Normalization")

right = input.int(10, "Divergence Look Right", minval = 0, group = "Divergence")
left = input.int(15, "Divergence Look Left", minval = 0, group = "Divergence")
upper_range = input.int(100, "Maximum Lookback", minval = 0, group = "Divergence")
lower_range = input.int(5, "Minimum Lookback", minval = 0, group = "Divergence")
labels = input.string("Symbol", "Show Labels", ["Disabled", "Symbol", "Text"], group = "Divergence")
enable_regular_bullish = input.bool(true, "Regular Bullish", group = "Divergence", inline = "Bld")
enable_hidden_bullish = input.bool(false, "Hidden Bullish", group = "Divergence", inline = "Bld")
enable_regular_bearish = input.bool(true, "Regular Bearish", group = "Divergence", inline = "Brd")
enable_hidden_bearish = input.bool(false, "Hidden Bearish", group = "Divergence", inline = "Brd")

show_signal = input.bool(true, "Show Signal", group = "Visibility")
show_chikou = input.bool(false, "Show Chikou", group = "Visibility")
show_conversion_base = input.bool(false, "Show Conversion and Base", group = "Visibility")
show_ma = input.bool(false, "Show Moving Average", group = "Visibility")
show_min_max = input.bool(true, "Show Min/Max", group = "Visibility")
show_kumo = input.string("Full", "Show Kumo", ["Full", "Current", "Disabled"], group = "Visibility")
show_kumo_lines = input.bool(false, "Show Kumbo Lines", group = "Visibility")

color_on_conversion = input.bool(true, "Color Signal by Conversion Cross", group = "Color")
signal_color = input.color(#F36B16, "Signal Color", group = "Color", inline = "Signal")
signal_width = input.int(2, "", minval = 1, maxval = 5, group = "Color", inline = "Signal")
kumo_bullish_color = input.color(#22EA70, "Kumo Color", group = "Color", inline = "Kumo")
kumo_bearish_color = input.color(#FF2F1C, "", group = 
```