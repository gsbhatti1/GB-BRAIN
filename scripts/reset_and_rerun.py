"""
GB-BRAIN — Reset and Re-run
Resets all strategies to 'pending' and clears old backtest results
so you can re-extract with v2 engine and get unique results.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.brain_db import connect

conn = connect()

# Count current state
old_bt = conn.execute("SELECT COUNT(*) FROM backtest_results").fetchone()[0]
old_strat = conn.execute("SELECT COUNT(*) FROM strategies").fetchone()[0]

# Reset strategies to pending
conn.execute("UPDATE strategies SET status = 'pending', parameters = NULL, indicators = NULL")
# Delete old backtest results (they were all identical anyway)
conn.execute("DELETE FROM backtest_results")
conn.commit()

print(f"RESET COMPLETE")
print(f"  Strategies reset to pending: {old_strat}")
print(f"  Old backtest results deleted: {old_bt}")
print(f"")
print(f"Now run:")
print(f"  python parse/extract_logic.py")
print(f"  python backtest/run_backtest.py --limit 200")
print(f"  python backtest/score_and_sort.py --report")

conn.close()
