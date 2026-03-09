# SOURCE: https://github.com/0xemmkty/QuantMuse
# FILE  : demo_llm_nlp_simple.py

#!/usr/bin/env python3
"""
简化版 LLM & NLP 功能演示
展示核心功能，无需API密钥
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_service.ai import NLPProcessor, SentimentFactorCalculator
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def demo_nlp_processing():
    """演示NLP处理功能"""
    print("🔍 演示NLP处理功能")
    print("=" * 50)
    
    # 初始化NLP处理器
    nlp_processor = NLPProcessor(use_spacy=False, use_transformers=False)
    
    # 示例文本
    sample_texts = [
        "Apple reports strong Q4 earnings, stock surges 5% on better-than-expected iPhone sales",
        "Tesla faces production challenges, shares decline due to supply chain issues",
        "Google announces revolutionary AI breakthrough that could transform the industry",
        "Market volatility increases as investors react to Fed policy changes"
    ]
    
    print("📝 处理示例文本:")
    for i, text in enumerate(sample_texts, 1):
        print(f"\n{i}. 原文: {text}")
        
        # 预处理文本
        processed = nlp_processor.preprocess_text(text)
        
        print(f"   清理后: {processed.cleaned_text[:100]}...")
        print(f"   关键词: {', '.join(processed.keywords[:5])}")
        print(f"   情感: {processed.sentiment_label} (得分: {processed.sentiment_score:.2f})")
        print(f"   主题: {', '.join(processed.topics[:3])}")

def demo_sentiment_factor():
    """演示情感因子生成"""
    print("\n📊 演示情感因子生成")
    print("=" * 50)
    
    # 初始化情感因子计算器
    sentiment_calculator = SentimentFactorCalculator()
    
    # 模拟情感数据
    sentiment_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 10,
        'date': pd.date_range('2024-01-01', periods=50, freq='D').repeat(5),
        'sentiment_score': np.random.normal(0, 0.3, 50),
        'volume': np.random.randint(100, 1000, 50),
        'source': ['news', 'twitter', 'reddit'] * 16 + ['news', 'twitter']
    })
    
    print("📈 生成情感因子:")
    
    # 计算各种情感因子
    factors = sentiment_calculator.calculate_sentiment_factors(sentiment_data)
    
    for factor_name, factor_data in factors.items():
        if isinstance(factor_data, dict):
            print(f"\n{factor_name}:")
            for symbol, value in list(factor_data.items())[:3]:  # 只显示前3个
                print(f"  {symbol}: {value:.4f}")
        else:
            print(f"{factor_name}: {factor_data:.4f}")

def demo_market_analysis():
    """演示市场分析功能"""
    print("\n🎯 演示市场分析功能")
    print("=" * 50)
    
    # 模拟市场数据
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    symbols = ['AAPL', 'GOOGL', 'TSLA']
    
    market_data = {}
    for symbol in symbols:
        base_price = np.random.uniform(100, 500)
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        market_data[symbol] = pd.DataFrame({
            'date': dates,
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        })
    
    # 模拟情感数据
    sentiment_data = pd.DataFrame({
        'symbol': symbols * 10,
        'date': pd.date_range('2024-01-01', periods=30, freq='D').repeat(len(symbols)),
        'sentiment_score': np.random.normal(0, 0.3, 30 * len(symbols)),
        'volume': np.random.randint(100, 1000, 30 * len(symbols))
    })
    
    print("📊 市场分析结果:")
    
    # 计算市场情绪指标
    sentiment_calculator = SentimentFactorCalculator()
    market_sentiment = sentiment_calculator.calculate_market_sentiment(sentiment_data)
    
    print(f"整体市场情绪: {market_sentiment['overall_sentiment']:.2f}")
    print(f"情绪波动性: {market_sentiment['sentiment_volatility']:.4f}")
    print(f"情绪一致性: {market_sentiment['sentiment_consensus']:.2f}")
    
    # 按股票分析
    print("\n各股票情绪分析:")
    for symbol in symbols:
        symbol_sentiment = sentiment_data[sentiment_data['symbol'] == symbol]['sentiment_score'].mean()
        print(f"  {symbol}: {symbol_sentiment:.3f}")

def demo_strategy_integration():
    """演示与策略系统的集成"""
    print("\n⚙️ 演示与策略系统集成")
    print("=" * 50)
    
    # 模拟因子数据
    factor_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 5,
        'date': pd.date_range('2024-01-01', periods=25, freq='D').repeat(5),
        'factor_name': ['sentiment_momentum', 'sentiment_volatility', 'news_volume', 'social_volume', 'sentiment_consensus'] * 5,
        'factor_value': np.random.normal(0, 1, 125)
    })
    
    # 模拟价格数据
    price_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 5,
        'date': pd.date_range('2024-01-01', periods=25, freq='D').repeat(5),
        'close': np.random.uniform(100, 500, 125)
    })
    
    print("🔗 情感因子与策略集成:")
    
    # 计算情感因子权重
    sentiment_factors = factor_data[factor_data['factor_name'].str.contains('sentiment')]
    
    print("情感因子统计:")
    for factor_name in sentiment_factors['factor_name'].unique():
        factor_values = sentiment_factors[sentiment_factors['factor_name'] == factor_name]['factor_value']
        print(f"  {factor_name}: 均值={factor_values.mean():.3f}, 标准差={factor_values.std():.3f}")
    
    # 模拟策略信号
    print("\n策略信号生成:")
    signals = []
    for symbol in ['AAPL', 'GOOGL', 'TSLA']:
        symbol_sentiment = sentiment_factors[sentiment_factors['symbol'] == symbol]['factor_value'].mean()
        
        if symbol_sentiment > 0.5:
            signal = "强烈买入"
        elif symbol_sentiment > 0:
            signal = "买入"
        elif symbol_sentiment > -0.5:
            signal = "持有"
        else:
            signal = "卖出"
        
        signals.append((symbol, symbol_sentiment, signal))
        print(f"  {symbol}: 情感得分={symbol_sentiment:.3f} → {signal}")

def main():
    """主函数"""
    setup_logging()
    
    print("🚀 LLM & NLP 扩展模块演示")
    print("=" * 60)
    
    try:
        # 演示各个功能模块
        demo_nlp_processing()
        demo_sentiment_factor()
        demo_market_analysis()
        demo_strategy_integration()
        
        print("\n✅ 演示完成！")
        print("\n📋 功能总结:")
        print("  • NLP文本处理: 清理、分词、关键词提取、情感分析")
        print("  • 情感因子生成: 动量、波动性、成交量、一致性")
        print("  • 市场分析: 整体情绪、个股情绪、趋势分析")
        print("  • 策略集成: 情感因子权重、交易信号生成")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 