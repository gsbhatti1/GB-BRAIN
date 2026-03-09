from pathlib import Path
source = len(list(Path(r'C:\Users\gsbha\qwen-dev\Trading-Strategies').rglob('*.md')))
translated = len(list(Path(r'C:\Users\gsbha\qwen-dev\Future-Trading\2_translated').rglob('*.md')))
left = source - translated
perc = round((translated / source) * 100, 2)
print(f'Translated : {translated}')
print(f'Total      : {source}')
print(f'Progress   : {perc}%')
print(f'Remaining  : {left}')