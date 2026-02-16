import pandas as pd

# Load datasets
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

print("=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

# Fear & Greed Index
print("\n📊 Bitcoin Fear & Greed Index (fear_greed.csv)")
print(f"  Records: {len(sentiment)}")
print(f"  Columns: {list(sentiment.columns)}")
print(f"  Null values: {sentiment.isnull().sum().sum()}")
print(f"  Duplicate rows: {sentiment.duplicated().sum()}")
print(f"  Date range: {sentiment['date'].min()} to {sentiment['date'].max()}")

# Hyperliquid Trades
print("\n🔄 Hyperliquid Trades (hyperliquid_trades.csv)")
print(f"  Records: {len(trades)}")
print(f"  Columns: {list(trades.columns)}")
print(f"  Null values: {trades.isnull().sum().sum()}")
print(f"  Duplicate rows: {trades.duplicated().sum()}")
if 'time' in trades.columns:
    print(f"  Date range: {trades['time'].min()} to {trades['time'].max()}")

# Type checks
print("\n✅ Data Type Validation")
print("\nFear & Greed Index:")
for col, dtype in sentiment.dtypes.items():
    print(f"  {col}: {dtype}")

print("\nHyperliquid Trades:")
for col, dtype in trades.dtypes.items():
    print(f"  {col}: {dtype}")

# Duplicate date checks
print("\n🔍 Duplicate Date Check (fear_greed.csv)")
dup_dates = sentiment['date'].value_counts()
if (dup_dates > 1).any():
    print(f"  ⚠️  Found {(dup_dates > 1).sum()} duplicate dates:")
    print(dup_dates[dup_dates > 1])
else:
    print("  ✅ No duplicate dates (unique index)")

print("\n" + "=" * 60)
