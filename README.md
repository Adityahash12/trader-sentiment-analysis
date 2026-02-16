# trader-sentiment-analysis# Bitcoin Fear & Greed Index: Impact on Hyperliquid Trader Behavior & Performance

## 🛠️ Setup & Execution
1. **Clone the Repo:** `git clone https://github.com/Aditya-Sarkar/trader-sentiment-analysis.git`
2. **Install Dependencies:** `pip install pandas matplotlib seaborn scikit-learn`
3. **Run Analysis:** - `python analysis.py` (Core performance & behavior analysis)
   - `python clustering_analysis.py` (Bonus ML: Trader Archetypes)

---

## Executive Summary
This analysis examines how Bitcoin market sentiment (Fear vs Greed Index) correlates with trader behavior and performance metrics on Hyperliquid. By merging daily sentiment data with historical trading data, we identify meaningful patterns in profitability, win rates, and leverage usage across different market sentiment regimes.

---

## Key Findings 📊

![Win Rate Comparison](outputs/02_win_rate.png)

### 1. Performance differs by sentiment
- **Extreme Fear Days:** Avg Daily PnL: **$70.00** | Win Rate: **80.0%**
- **Fear Days:** Avg Daily PnL: **$21.83** | Win Rate: **33.3%**
- **Insight:** Paradoxically, traders performed better on Extreme Fear days, likely due to forced liquidations of weak hands and high volatility.

### 2. Behavior changes during Fear 📉
- Win rate drops significantly (**80% → 33%**) during Fear.
- This suggests reactive or emotional trading rather than systematic execution during standard fear periods.

---

## Strategy Recommendations 🎯

### 1. During Fear Days: De-leverage
- **Action:** Cap leverage at **2.0x** for high-frequency traders.
- **Rationale:** Fear periods show degraded win rates (33%), suggesting poor fills or slippage.

### 2. During Greed Days: Optimize Scaling
- **Action:** Allow leverage up to **3.5x** for historically profitable traders.
- **Rationale:** High leverage traders profited during Extreme Fear; they have the skill to use leverage effectively.

---

## Bonus: Trader Clustering (Archetypes)
Beyond standard segmentation, this repository includes a **K-Means Clustering** implementation to identify:
- **Revenge Traders:** High frequency/leverage during Fear.
- **Tactical Scalpers:** High leverage only during Extreme volatility.
- **Conservative Accumulators:** Stable, low-risk profiles.
