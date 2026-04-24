![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)

# US Equity Sector Rotation Analysis

Track 2 GitHub Data Analysis Project focused on whether major US equity sectors rotate across different macro regimes.

**Demo Video (Mediasite):** <!-- TODO: insert Mediasite link here before submission -->

Performance snapshot across the full 2020–2024 analysis period:

| Metric | Result |
|---|---|
| Best full-period sector | **Technology** (160.5% total return) |
| Weakest full-period sector | **Health Care** (45.9% total return) |
| 2022 defensive winner | **Energy** (64.3%) |
| 2023 rebound leader | **Technology** (56.0%) |

<p align="center">
  <img src="figures/cumulative_returns.png" alt="Cumulative returns chart" width="48%" />
  <img src="figures/annual_returns_heatmap.png" alt="Annual returns heatmap" width="48%" />
</p>

## 1. Problem & User

This project asks whether sector performance follows a rotation pattern across three distinct macro regimes — the pandemic shock, the 2022 rate-hike cycle, and the 2023-2024 recovery. Retail investors often hold static sector weights, yet evidence suggests that leadership shifts materially between cyclical phases; understanding these shifts can help investors adjust allocations proactively rather than reactively. The target users are individual investors who allocate across sector ETFs and finance or economics students seeking a practical, visual introduction to cross-sector leadership dynamics. For these users, a clear analytical narrative supported by reproducible code is more valuable than a black-box trading signal.

## 2. Data

- Source: Yahoo Finance via the `yfinance` Python package
- Access date: 2026-04-21
- Analysis window: 2020-01-01 to 2024-12-31
- Frequency: daily adjusted close prices, transformed into daily / monthly / quarterly returns
- Key fields: `Close` (adjusted for dividends and splits) per ETF

| ETF | Sector |
|---|---|
| `XLK` | Technology |
| `XLY` | Consumer Discretionary |
| `XLE` | Energy |
| `XLV` | Health Care |
| `XLF` | Financials |

Generated datasets are stored in `data/`, including daily prices, daily returns, monthly returns, annual returns, rolling volatility, correlation matrix, and yearly rankings.

**Data compliance:** Yahoo Finance data accessed via `yfinance` is publicly available market data. Its use for non-commercial, educational analysis is consistent with Yahoo's Terms of Service. The data source and access date are stated above as required.

## 3. Methods

- Download adjusted close prices for five representative US sector ETFs via `yfinance.download()`, with retry logic and fallback tickers for robustness
- Clean missing values with forward fill (`ffill`) and align all series on common trading days via `pd.concat`
- Compute daily returns with `pct_change()` and monthly returns with `resample('ME')` — multiple frequencies capture both short-term and medium-term rotation patterns
- Compare cumulative returns across sectors using `(1 + daily_returns).cumprod() - 1`
- Build annual and quarterly return heatmaps with `seaborn` — heatmaps enable rapid visual identification of which sectors outperform or underperform in each period
- Measure cross-sector correlation via `df.corr()` on daily returns — correlation reveals co-movement patterns and diversification potential
- Estimate 30-day rolling annualised volatility (`rolling(30).std() * sqrt(252)`) — the 30-day window balances responsiveness and smoothness
- Rank the strongest and weakest sector each year using `groupby` and descending sort

## 4. Key Findings

Findings below are derived from the complete analytical workflow in `notebook.ipynb` and can be reproduced by running all cells.

- In 2022, Energy was the only clear defensive winner, returning 64.3%, while Consumer Discretionary dropped 36.3%.
- The 2023 rebound was led by Technology, which gained 56.0% as growth assets recovered.
- Across the full 2020-2024 window, Technology delivered the highest total return at 160.5%, while Health Care lagged at 45.9%.
- The tightest daily co-movement came from Technology and Consumer Discretionary, with a correlation of 0.84, indicating strong cyclical overlap and limited diversification benefit.
- Sector leadership changed materially between the pandemic shock, the 2022 hiking cycle, and the 2023-2024 recovery, which supports a rotation-based allocation lens.

## 5. Visual Preview

<p align="center">
  <img src="figures/quarterly_returns_heatmap.png" alt="Quarterly returns heatmap" width="48%" />
  <img src="figures/correlation_heatmap.png" alt="Correlation heatmap" width="48%" />
</p>

## 6. Limitations & Next Steps

- Sector ETFs are proxies that may not fully capture intra-sector heterogeneity (e.g., small-cap vs large-cap behaviour within a sector).
- Yahoo Finance data is adequate for educational analysis but does not match the quality or completeness of professional terminals such as Bloomberg.
- The analysis is purely descriptive — no causal or predictive model is estimated, so rotation explanations remain empirically grounded rather than statistically validated.
- **Next steps:** incorporate macroeconomic indicators (interest rates, inflation, oil prices) as exogenous variables, implement a sector-rotation strategy backtest with transaction costs, and extend coverage to additional sectors (e.g., XLRE, XLB).

## 7. How to Run

### Option A: pip

```bash
pip3 install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

### Option B: Conda

```bash
conda env create -f environment.yml
conda activate acc102_track2
python scripts/build_artifacts.py   # downloads data & saves CSVs to data/
python scripts/generate_notebook.py # populates notebook from src/ module
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

After execution, check the `data/` and `figures/` directories for generated outputs.

### Optional Streamlit demo

```bash
streamlit run streamlit_app.py
```

> Note: The Streamlit app is a supplementary interface. The primary deliverable for marking is `notebook.ipynb`.

## 8. Repository Structure

```text
.
|-- README.md
|-- notebook.ipynb
|-- reflection_report.md
|-- requirements.txt
|-- environment.yml
|-- streamlit_app.py
|-- data/
|-- figures/
|-- reports/
|-- scripts/
`-- src/
```
