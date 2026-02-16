import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory for files
os.makedirs("outputs", exist_ok=True)

# Load datasets
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

print("Sentiment shape:", sentiment.shape)
print("Trades shape:", trades.shape)

# Clean sentiment data
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date
sentiment.rename(columns={'classification': 'Classification'}, inplace=True)

# Clean trade data
trades['time'] = pd.to_datetime(trades['time'])
trades['date'] = trades['time'].dt.date

# Merge datasets
merged = trades.merge(
    sentiment[['date', 'Classification']],
    on='date',
    how='inner'
)

print("Merged shape:", merged.shape)

# Create daily metrics
daily_metrics = merged.groupby(
    ['account', 'date', 'Classification']
).agg(
    daily_pnl=('closedPnL', 'sum'),
    trades_count=('closedPnL', 'count'),
    avg_leverage=('leverage', 'mean'),
    avg_size=('size', 'mean'),
    win_rate=('closedPnL', lambda x: (x > 0).mean())
).reset_index()

print("\nDaily Metrics (first 5 rows):")
print(daily_metrics.head())

# Save daily metrics
daily_metrics.to_csv("outputs/daily_metrics.csv", index=False)
print("✓ Saved daily_metrics.csv")

# Fear vs Greed summary
summary = daily_metrics.groupby('Classification').agg({
    'daily_pnl': 'mean',
    'trades_count': 'mean',
    'avg_leverage': 'mean',
    'avg_size': 'mean',
    'win_rate': 'mean'
}).round(4)

print("\nFear vs Greed Summary:")
print(summary)

# Save summary table
summary.to_csv("outputs/fear_vs_greed_summary.csv")
print("✓ Saved fear_vs_greed_summary.csv")

# ============ PLOT 1: Avg Daily PnL ============
plt.figure(figsize=(10, 6))
summary['daily_pnl'].plot(kind='bar', color=['#FF6B6B', '#4ECDC4'], title='Average Daily PnL: Fear vs Greed', fontsize=12)
plt.ylabel('Avg Daily PnL ($)', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/01_avg_daily_pnl.png", dpi=300, bbox_inches='tight')
print("✓ Saved 01_avg_daily_pnl.png")
plt.close()

# ============ PLOT 2: Win Rate ============
plt.figure(figsize=(10, 6))
summary['win_rate'].plot(kind='bar', color=['#FF6B6B', '#4ECDC4'], title='Win Rate: Fear vs Greed', fontsize=12)
plt.ylabel('Win Rate (%)', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.ylim([0, 1])
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/02_win_rate.png", dpi=300, bbox_inches='tight')
print("✓ Saved 02_win_rate.png")
plt.close()

# ============ PLOT 3: Avg Leverage ============
plt.figure(figsize=(10, 6))
summary['avg_leverage'].plot(kind='bar', color=['#FF6B6B', '#4ECDC4'], title='Average Leverage: Fear vs Greed', fontsize=12)
plt.ylabel('Avg Leverage', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/03_avg_leverage.png", dpi=300, bbox_inches='tight')
print("✓ Saved 03_avg_leverage.png")
plt.close()

# ============ PLOT 4: Trade Count ============
plt.figure(figsize=(10, 6))
summary['trades_count'].plot(kind='bar', color=['#FF6B6B', '#4ECDC4'], title='Average Trades per Day: Fear vs Greed', fontsize=12)
plt.ylabel('Avg Trade Count', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/04_trades_per_day.png", dpi=300, bbox_inches='tight')
print("✓ Saved 04_trades_per_day.png")
plt.close()

# ============ PLOT 5: Leverage Distribution (Boxplot) ============
plt.figure(figsize=(10, 6))
sns.boxplot(data=daily_metrics, x='Classification', y='avg_leverage', palette=['#FF6B6B', '#4ECDC4'], hue='Classification', legend=False)
plt.title('Leverage Distribution by Market Sentiment', fontsize=12)
plt.ylabel('Avg Leverage', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/05_leverage_distribution.png", dpi=300, bbox_inches='tight')
print("✓ Saved 05_leverage_distribution.png")
plt.close()

# ============ PLOT 6: PnL Distribution (Boxplot) ============
plt.figure(figsize=(10, 6))
sns.boxplot(data=daily_metrics, x='Classification', y='daily_pnl', palette=['#FF6B6B', '#4ECDC4'], hue='Classification', legend=False)
plt.title('PnL Distribution by Market Sentiment', fontsize=12)
plt.ylabel('Daily PnL ($)', fontsize=11)
plt.xlabel('Market Sentiment', fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/06_pnl_distribution.png", dpi=300, bbox_inches='tight')
print("✓ Saved 06_pnl_distribution.png")
plt.close()

# Trader segmentation
median_leverage = daily_metrics['avg_leverage'].median()

daily_metrics['leverage_group'] = np.where(
    daily_metrics['avg_leverage'] > median_leverage,
    'High Leverage',
    'Low Leverage'
)

segment_analysis = daily_metrics.groupby(
    ['leverage_group', 'Classification']
)['daily_pnl'].mean().unstack(fill_value=0)

print("\nSegment Analysis (High/Low Leverage):")
print(segment_analysis)

# Save segment analysis
segment_analysis.to_csv("outputs/segment_analysis.csv")
print("✓ Saved segment_analysis.csv")

# ============ PLOT 7: Segment Analysis ============
plt.figure(figsize=(10, 6))
segment_analysis.plot(kind='bar', color=['#FF6B6B', '#4ECDC4'], ax=plt.gca())
plt.title('Avg PnL by Leverage Group & Market Sentiment', fontsize=12)
plt.ylabel('Avg PnL ($)', fontsize=11)
plt.xlabel('Leverage Group', fontsize=11)
plt.legend(title='Market Sentiment', fontsize=10)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/07_segment_analysis.png", dpi=300, bbox_inches='tight')
print("✓ Saved 07_segment_analysis.png")
plt.close()

print("\n" + "="*50)
print("✅ Analysis complete! All outputs saved to ./outputs/")
print("="*50)
print("\nGenerated files:")
print("📊 Tables (CSV):")
print("  - daily_metrics.csv")
print("  - fear_vs_greed_summary.csv")
print("  - segment_analysis.csv")
print("\n📈 Plots (PNG):")
print("  - 01_avg_daily_pnl.png")
print("  - 02_win_rate.png")
print("  - 03_avg_leverage.png")
print("  - 04_trades_per_day.png")
print("  - 05_leverage_distribution.png")
print("  - 06_pnl_distribution.png")
print("  - 07_segment_analysis.png")
