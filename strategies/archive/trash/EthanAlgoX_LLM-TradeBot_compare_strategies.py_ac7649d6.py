# SOURCE: https://github.com/EthanAlgoX/LLM-TradeBot
# FILE  : compare_strategies.py

#!/usr/bin/env python3
"""
策略对比回测脚本
比较默认策略 vs 优化V2策略
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.backtest.engine import BacktestEngine, BacktestConfig
from src.strategies.optimized_v2 import strategy_v2_wrapper, StrategyConfig


async def run_strategy_comparison(
    symbol: str = "SOLUSDT",  # 使用之前表现最好的币种
    days: int = 1
):
    """运行策略对比"""
    
    end_date = datetime.now() - timedelta(days=1)  # 使用昨天作为结束，避免数据不完整
    start_date = end_date - timedelta(days=days)
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print("\n" + "="*70)
    print("🔬 策略对比回测")
    print("="*70)
    print(f"📊 币种: {symbol}")
    print(f"📅 周期: {start_str} to {end_str}")
    print(f"💰 初始资金: $10,000")
    print("="*70)
    
    results = []
    
    # 1️⃣ 测试默认策略 (technical)
    print("\n📈 1. 测试默认策略 (Technical)...")
    
    config1 = BacktestConfig(
        symbol=symbol,
        start_date=start_str,
        end_date=end_str,
        initial_capital=10000,
        step=3,
        strategy_mode="technical",
    )
    
    try:
        engine1 = BacktestEngine(config1)
        result1 = await engine1.run()
        results.append({
            'name': 'Default (Technical)',
            'return': result1.metrics.total_return,
            'win_rate': result1.metrics.win_rate,
            'trades': result1.metrics.total_trades,
            'sharpe': result1.metrics.sharpe_ratio,
            'max_dd': result1.metrics.max_drawdown_pct,
        })
        print(f"   ✅ 收益率: {result1.metrics.total_return:+.2f}%")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        results.append({
            'name': 'Default (Technical)',
            'return': None,
            'error': str(e)
        })
    
    # 2️⃣ 测试优化V2策略
    print("\n📈 2. 测试优化V2策略...")
    
    config2 = BacktestConfig(
        symbol=symbol,
        start_date=start_str,
        end_date=end_str,
        initial_capital=10000,
        step=3,
        strategy_mode="technical",  # 使用technical模式但注入自定义策略
    )
    
    try:
        engine2 = BacktestEngine(config2)
        # 注入优化策略
        engine2.strategy_fn = strategy_v2_wrapper
        
        result2 = await engine2.run()
        results.append({
            'name': 'Optimized V2',
            'return': result2.metrics.total_return,
            'win_rate': result2.metrics.win_rate,
            'trades': result2.metrics.total_trades,
            'sharpe': result2.metrics.sharpe_ratio,
            'max_dd': result2.metrics.max_drawdown_pct,
        })
        print(f"   ✅ 收益率: {result2.metrics.total_return:+.2f}%")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        results.append({
            'name': 'Optimized V2',
            'return': None,
            'error': str(e)
        })
    
    # 3️⃣ 测试激进版V2策略 (更低入场门槛)
    print("\n📈 3. 测试激进V2策略 (低门槛)...")
    
    config3 = BacktestConfig(
        symbol=symbol,
        start_date=start_str,
        end_date=end_str,
        initial_capital=10000,
        step=3,
        strategy_mode="technical",
    )
    
    # 创建激进配置
    aggressive_config = StrategyConfig(
        rsi_oversold=40,  # 更宽松
        rsi_overbought=60,
        ema_fast=5,  # 更快
        ema_slow=13,
        rvol_threshold=1.0,  # 不要求高成交量
    )
    
    async def aggressive_strategy(snapshot, portfolio, current_price, config):
        from src.strategies.optimized_v2 import optimized_strategy_v2
        return optimized_strategy_v2(snapshot, portfolio, current_price, config, aggressive_config)
    
    try:
        engine3 = BacktestEngine(config3)
        engine3.strategy_fn = aggressive_strategy
        
        result3 = await engine3.run()
        results.append({
            'name': 'Aggressive V2',
            'return': result3.metrics.total_return,
            'win_rate': result3.metrics.win_rate,
            'trades': result3.metrics.total_trades,
            'sharpe': result3.metrics.sharpe_ratio,
            'max_dd': result3.metrics.max_drawdown_pct,
        })
        print(f"   ✅ 收益率: {result3.metrics.total_return:+.2f}%")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        results.append({
            'name': 'Aggressive V2',
            'return': None,
            'error': str(e)
        })
    
    # 打印对比结果
    print("\n" + "="*70)
    print("📊 策略对比结果")
    print("="*70)
    
    print(f"\n{'策略名称':<20} {'收益率':>10} {'胜率':>10} {'交易次数':>10} {'Sharpe':>10} {'最大回撤':>10}")
    print("-"*70)
    
    for r in results:
        if r.get('return') is not None:
            print(f"{r['name']:<20} {r['return']:>+9.2f}% {r['win_rate']:>9.1f}% {r['trades']:>10} {r['sharpe']:>10.2f} {r['max_dd']:>9.2f}%")
        else:
            print(f"{r['name']:<20} {'ERROR':>10}")
    
    # 找出最佳策略
    valid_results = [r for r in results if r.get('return') is not None]
    if valid_results:
        best = max(valid_results, key=lambda x: x['return'])
        print("\n" + "="*70)
        print(f"🏆 最佳策略: {best['name']}")
        print(f"   收益率: {best['return']:+.2f}%")
        print(f"   胜率: {best['win_rate']:.1f}%")
        print(f"   交易次数: {best['trades']}")
        print("="*70)
    
    return results


async def run_multi_symbol_comparison():
    """多币种对比测试"""
    
    symbols = ["SOLUSDT", "BTCUSDT", "ETHUSDT"]
    all_results = {}
    
    for symbol in symbols:
        print(f"\n\n{'#'*70}")
        print(f"# 测试币种: {symbol}")
        print(f"{'#'*70}")
        
        results = await run_strategy_comparison(symbol=symbol, days=1)
        all_results[symbol] = results
    
    # 汇总
    print("\n\n" + "="*70)
    print("📊 多币种策略汇总")
    print("="*70)
    
    for symbol, results in all_results.items():
        print(f"\n{symbol}:")
        for r in results:
            if r.get('return') is not None:
                print(f"  {r['name']}: {r['return']:+.2f}%")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="策略对比回测")
    parser.add_argument("--symbol", type=str, default="SOLUSDT", help="交易对")
    parser.add_argument("--days", type=int, default=1, help="回测天数")
    parser.add_argument("--multi", action="store_true", help="多币种测试")
    
    args = parser.parse_args()
    
    if args.multi:
        asyncio.run(run_multi_symbol_comparison())
    else:
        asyncio.run(run_strategy_comparison(symbol=args.symbol, days=args.days))
