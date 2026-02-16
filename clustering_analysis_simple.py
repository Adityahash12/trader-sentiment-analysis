"""
BONUS: Simple Trader Segmentation (No Sklearn Required)
Demonstrates how to categorize traders into behavioral archetypes.
"""

import pandas as pd
import numpy as np

# Load data
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

# Prepare data
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date
sentiment.rename(columns={'classification': 'Classification'}, inplace=True)

trades['time'] = pd.to_datetime(trades['time'])
trades['date'] = trades['time'].dt.date

# Merge
merged = trades.merge(
    sentiment[['date', 'Classification']],
    on='date',
    how='inner'
)

# Create trader profiles
trader_profiles = merged.groupby('account').agg({
    'closedPnL': ['sum', 'mean', 'std'],
    'leverage': 'mean',
    'size': 'mean',
    'date': 'count',  # trade frequency
}).reset_index()

trader_profiles.columns = ['account', 'total_pnl', 'avg_pnl', 'std_pnl', 'avg_leverage', 'avg_size', 'trade_count']

# Calculate win rate per trader
def calc_win_rate(acct):
    acct_trades = merged[merged['account'] == acct]['closedPnL']
    return (acct_trades > 0).mean() if len(acct_trades) > 0 else 0

trader_profiles['win_rate'] = trader_profiles['account'].apply(calc_win_rate)

# Calculate sentiment reaction (leverage during Fear vs other)
def calc_sentiment_reaction(acct):
    acct_data = merged[merged['account'] == acct]
    fear_trades = acct_data[acct_data['Classification'].str.contains('Fear', na=False)]
    other_trades = acct_data[~acct_data['Classification'].str.contains('Fear', na=False)]
    
    fear_lev = fear_trades['leverage'].mean() if len(fear_trades) > 0 else 0
    other_lev = other_trades['leverage'].mean() if len(other_trades) > 0 else 0
    
    return fear_lev - other_lev

trader_profiles['sentiment_reaction'] = trader_profiles['account'].apply(calc_sentiment_reaction)

print("=" * 70)
print("TRADER PROFILES (Raw Metrics)")
print("=" * 70)
print(trader_profiles.to_string(index=False))

# Simple rule-based clustering
def classify_trader(row):
    lev = row['avg_leverage']
    win_rt = row['win_rate']
    sent_react = row['sentiment_reaction']
    trade_ct = row['trade_count']
    
    # Rules for archetype classification
    if sent_react > 0.2 and trade_ct >= 2:
        return "Revenge Trader (Reactive)"
    elif lev > 3.0 and win_rt < 0.5:
        return "Risk Taker (High Leverage, Mixed Results)"
    elif win_rt > 0.5 and lev < 2.5:
        return "Conservative Accumulator"
    elif sent_react > 0.1 and lev > 3.0:
        return "Tactical Scalper (Volatility Sensitive)"
    else:
        return "Balanced Trader"

trader_profiles['archetype'] = trader_profiles.apply(classify_trader, axis=1)

print("\n" + "=" * 70)
print("TRADER ARCHETYPES (Behavioral Classification)")
print("=" * 70)
print(trader_profiles[['account', 'archetype', 'avg_leverage', 'win_rate', 'sentiment_reaction']].to_string(index=False))

# Summary by archetype
print("\n" + "=" * 70)
print("ARCHETYPE SUMMARY & RECOMMENDATIONS")
print("=" * 70)

for archetype in trader_profiles['archetype'].unique():
    arch_traders = trader_profiles[trader_profiles['archetype'] == archetype]
    print(f"\n🎯 {archetype}")
    print(f"   Accounts: {', '.join(arch_traders['account'].tolist())}")
    print(f"   Avg Leverage: {arch_traders['avg_leverage'].mean():.2f}x")
    print(f"   Avg Win Rate: {(arch_traders['win_rate'].mean()*100):.1f}%")
    print(f"   Sentiment Reaction: {arch_traders['sentiment_reaction'].mean():.2f}")
    print(f"   Avg PnL: ${arch_traders['avg_pnl'].mean():.2f}")
    
    # Recommendations
    if "Revenge" in archetype:
        print(f"   💡 Action: Cap leverage at 1.5x during Fear; monitor daily drawdown")
    elif "Risk Taker" in archetype:
        print(f"   💡 Action: Implement max 3.5x leverage cap; require approval for > 2x")
    elif "Conservative" in archetype:
        print(f"   💡 Action: Allow higher leverage up to 3.5x; stable allocation")
    elif "Tactical" in archetype:
        print(f"   💡 Action: Leverage allowed up to 4.0x during volatility; monitor closely")
    else:
        print(f"   💡 Action: Standard leverage policy (2.0x-3.0x)")

print("\n" + "=" * 70)
print("✅ Behavioral Segmentation Complete!")
print("   Use these archetypes to design personalized risk policies.")
print("=" * 70)

# Save results
trader_profiles.to_csv("outputs/clustering_simple_results.csv", index=False)
print("\n✓ Saved clustering_simple_results.csv")
