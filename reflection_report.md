# ACC102 Track 2 — Reflection Report

## 1. Problem Analysis and Target User Identification

This project investigates whether major US equity sectors exhibit rotation patterns across different macroeconomic regimes. Retail investors often treat sector allocation as static, yet evidence suggests that leadership shifts materially between cyclical phases — the pandemic crash, the 2022 rate-hiking cycle, and the subsequent recovery. Understanding these shifts helps investors adjust exposure proactively. The target users are individual investors who allocate across sector ETFs and finance students seeking a data-driven introduction to sector-level market behaviour. For these users, a clear analytical narrative supported by reproducible code is more valuable than a black-box signal.

## 2. Dataset Introduction and Selection Rationale

The dataset consists of daily adjusted closing prices for five SPDR sector ETFs — XLK (Technology), XLY (Consumer Discretionary), XLE (Energy), XLV (Health Care), and XLF (Financials) — retrieved from Yahoo Finance via `yfinance`. The window spans January 2020 to December 2024, covering approximately 1,260 trading days with one date index and five price columns. This dataset was selected because: (1) sector ETFs aggregate hundreds of constituents, reducing single-stock noise; (2) Yahoo Finance is freely accessible and requires no API key, ensuring full reproducibility for a GitHub-hosted project; (3) the 2020–2024 period encompasses the COVID-19 shock, monetary tightening, and an AI-driven growth rebound, providing natural variation to observe rotation.Data were accessed on **21 April 2026** from Yahoo Finance using the yfinance library.

## 3. Python Methodology Explanation

The workflow proceeds in four stages. Data acquisition uses `yfinance.download()` with a retry mechanism and fallback tickers (e.g., VDE for XLE). Cleaning applies forward-fill for isolated gaps and aligns all series on common trading days via `pd.concat`. Returns are computed at daily (`pct_change()`), monthly (`resample('ME').last().pct_change()`), and quarterly frequencies. Cumulative returns use `(1 + daily_returns).cumprod() - 1`. Cross-sector correlation is derived from `df.corr()` on daily returns. Rolling annualised volatility is calculated as `daily_returns.rolling(30).std() * sqrt(252)`. Yearly rankings employ `groupby` on annual returns with descending sort. All figures are rendered via `matplotlib` with a custom style dictionary and saved at 220 DPI; intermediate tables are exported as CSV for reproducibility.I also built a GitHub repository with a complete README, organized code structure, and clear documentation to ensure reproducibility. This process helped me understand how to present data work professionally for external users.

## 4. Key Insights Summary

Five findings emerged. (1) In 2022, Energy returned 64.3% while Consumer Discretionary fell 36.3%, the most dramatic divergence in the sample. (2) Technology led the 2023 rebound at 56.0%, confirming that growth assets recover when rate pressure eases. (3) Over the full window, Technology achieved the highest total return (160.5%) and Health Care the lowest (45.9%). (4) Technology and Consumer Discretionary showed the strongest daily co-movement (correlation 0.84), implying limited diversification within the cyclical pair. (5) Sector leadership changed materially across macro regimes, supporting a rotation-based rather than buy-and-hold perspective.

## 5. Limitations, Reliability Assessment, and Improvement Directions

Several limitations apply. Sector ETFs are proxies that may not capture intra-sector heterogeneity. Yahoo Finance data, while adequate for educational analysis, does not match professional terminals in quality. The analysis is purely descriptive — no causal or predictive model is estimated, so rotation explanations remain empirically grounded rather than statistically validated. Future work should incorporate macroeconomic indicators (interest rates, inflation, oil prices) as exogenous variables, implement a sector-rotation backtest with transaction costs, and extend coverage to additional sectors such as Real Estate (XLRE) or Materials (XLB).

## 6. Personal Contributions, Decision-Making Process, and Learning Outcomes

I defined the research question, selected the dataset and ETF universe, designed the analytical framework, and wrote all Python code. Key decisions included choosing a 30-day rolling window for volatility (balancing responsiveness and smoothness), selecting seaborn heatmaps for period-over-period comparison, and structuring the repository for one-click reproducibility. Through this project, I deepened my understanding of financial time-series manipulation, the importance of matching visualisation choices to the audience, and the discipline of organising code into modular, reproducible functions.

***

## AI Disclosure

I used two AI tools to support this project.

1. Trae AI (Claude 3.5 Sonnet), accessed on 21 April 2026, for project structure design, Python code generation, README drafting, and reflection report refinement.
2. OpenAI GPT-4o, accessed on 21 April 2026, for debugging yfinance data alignment and suggesting visualization color palettes.

   All analytical conclusions were independently verified. I take full responsibility for the final work.All analytical conclusions were independently verified against the data. I take full responsibility for the final content and any errors.

