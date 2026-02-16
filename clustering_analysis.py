"""
BONUS: K-Means Clustering for Trader Archetypes
Demonstrates how to segment traders into behavioral groups.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

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
    fear_lev = acct_data[acct_data['Classification'].str.contains('Fear', na=False)]['leverage'].mean()
    other_lev = acct_data[~acct_data['Classification'].str.contains('Fear', na=False)]['leverage'].mean()
    
    if pd.isna(fear_lev) or pd.isna(other_lev):
        return 0
    return fear_lev - other_lev

trader_profiles['sentiment_reaction'] = trader_profiles['account'].apply(calc_sentiment_reaction)

print("=" * 70)
print("TRADER PROFILES (before clustering)")
print("=" * 70)
print(trader_profiles.to_string(index=False))

# Prepare features for clustering
features = ['avg_leverage', 'trade_count', 'win_rate', 'sentiment_reaction', 'avg_pnl']
X = trader_profiles[features].fillna(0)

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means clustering (k=3, reasonable for 3 accounts)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
trader_profiles['cluster'] = kmeans.fit_predict(X_scaled)

print("\n" + "=" * 70)
print("CLUSTERED TRADER PROFILES")
print("=" * 70)
print(trader_profiles.to_string(index=False))

# Interpret clusters
print("\n" + "=" * 70)
print("CLUSTER INTERPRETATIONS")
print("=" * 70)

cluster_names = {
    0: "Cluster 0",
    1: "Cluster 1",
    2: "Cluster 2"
}

for cluster_id in sorted(trader_profiles['cluster'].unique()):
    cluster_data = trader_profiles[trader_profiles['cluster'] == cluster_id]
    print(f"\n🎯 {cluster_names[cluster_id]}")
    print(f"   Accounts: {', '.join(cluster_data['account'].tolist())}")
    print(f"   Avg Leverage: {cluster_data['avg_leverage'].mean():.2f}x")
    print(f"   Trade Count: {cluster_data['trade_count'].mean():.1f}")
    print(f"   Win Rate: {(cluster_data['win_rate'].mean()*100):.1f}%")
    print(f"   Sentiment Reaction: {cluster_data['sentiment_reaction'].mean():.2f}")
    print(f"   Avg PnL: ${cluster_data['avg_pnl'].mean():.2f}")
    
    # Characterize
    avg_lev = cluster_data['avg_leverage'].mean()
    win_rt = cluster_data['win_rate'].mean()
    sentiment_react = cluster_data['sentiment_reaction'].mean()
    
    if avg_lev > 3.0 and win_rt < 0.5:
        print(f"   📊 Profile: **High Risk Taker** (high leverage, lower win rate)")
    elif avg_lev > 2.5 and sentiment_react > 0.3:
        print(f"   📊 Profile: **Reactive Trader** (increases leverage during fear)")
    elif win_rt > 0.5 and avg_lev < 2.5:
        print(f"   📊 Profile: **Consistent Accumulator** (steady performance)")
    else:
        print(f"   📊 Profile: **Mixed Strategy**")

print("\n" + "=" * 70)
print("✅ Clustering complete! Use these groups for dynamic risk policies:")
print("   - Restrict leverage for high-risk clusters during Fear")
print("   - Allow higher leverage for consistent performers during Greed")
print("   - Monitor behavioral changes (e.g., sudden shift to reactive trading)")
print("=" * 70)

# Save results
trader_profiles.to_csv("outputs/clustering_results.csv", index=False)
print("\n✓ Saved clustering_results.csv")
