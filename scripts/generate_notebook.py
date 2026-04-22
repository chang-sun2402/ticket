from __future__ import annotations

from pathlib import Path
import sys

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sector_rotation_analysis import ACCESS_DATE, END_DATE, START_DATE, TICKER_MAP  # noqa: E402


def build_notebook() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    tickers = ", ".join(f"`{ticker}`" for ticker in TICKER_MAP)
    sector_names = ", ".join(TICKER_MAP.values())

    cells = [
        nbf.v4.new_markdown_cell(
            f"""# Sector Rotation Analysis: US Equity ETFs (2020-2024)

**Track 2 – GitHub Data Analysis Project**

- Problem: Do sector returns rotate across macro regimes, and which sectors lead under different market conditions?
- Target users: retail investors and finance/economics students
- Universe: {sector_names}
- Proxy ETFs: {tickers}
- Data source: Yahoo Finance via `yfinance`
- Analysis window: {START_DATE} to {END_DATE}
- Access date: {ACCESS_DATE}
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 1. Setup

This notebook follows the required structure from the project plan:

1. Download sector ETF data
2. Clean prices and compute daily/monthly returns
3. Compare cumulative returns, annual and quarterly heatmaps, correlation, and rolling volatility
4. Rank yearly winners and laggards
5. Summarize actionable findings
"""
        ),
        nbf.v4.new_code_cell(
            """from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Image, display

from src.sector_rotation_analysis import (
    ACCESS_DATE,
    END_DATE,
    START_DATE,
    TICKER_MAP,
    build_analysis,
    configure_plot_style,
    plot_annual_heatmap,
    plot_correlation_heatmap,
    plot_cumulative_returns,
    plot_quarterly_heatmap,
    plot_rolling_volatility,
    plot_yearly_winners,
)

root = Path.cwd()
bundle = build_analysis(root)
configure_plot_style()
bundle.prices.head()
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 2. Data Overview

The adjusted close series are forward-filled after download and then aligned on common trading days.
The transformed outputs are also saved to `data/` so the GitHub repository includes reproducible artifacts.
"""
        ),
        nbf.v4.new_code_cell(
            """display(bundle.prices.tail())
display(bundle.daily_returns.describe().T[["mean", "std", "min", "max"]].sort_values("mean", ascending=False))
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 3. Cumulative Return Comparison

This chart answers the most direct question: which sector created the most value over the full five-year period?
"""
        ),
        nbf.v4.new_code_cell(
            """plot_cumulative_returns(bundle, root / "figures" / "cumulative_returns.png")
display(Image(filename=str(root / "figures" / "cumulative_returns.png")))
display(bundle.summary_metrics.style.format("{:.1%}"))
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 4. Annual and Quarterly Rotation Heatmaps

The annual heatmap highlights regime shifts from year to year, while the quarterly heatmap shows shorter rotation cycles.
"""
        ),
        nbf.v4.new_code_cell(
            """plot_annual_heatmap(bundle, root / "figures" / "annual_returns_heatmap.png")
plot_quarterly_heatmap(bundle, root / "figures" / "quarterly_returns_heatmap.png")
display(Image(filename=str(root / "figures" / "annual_returns_heatmap.png")))
display(Image(filename=str(root / "figures" / "quarterly_returns_heatmap.png")))
display(bundle.annual_returns.style.format("{:.1%}"))
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 5. Correlation and Risk

Correlation shows which sectors move together. Rolling volatility adds a risk lens and shows where uncertainty spiked.
"""
        ),
        nbf.v4.new_code_cell(
            """plot_correlation_heatmap(bundle, root / "figures" / "correlation_heatmap.png")
plot_rolling_volatility(bundle, root / "figures" / "rolling_volatility.png")
display(Image(filename=str(root / "figures" / "correlation_heatmap.png")))
display(Image(filename=str(root / "figures" / "rolling_volatility.png")))
display(bundle.correlation_matrix.style.format("{:.2f}"))
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 6. Yearly Winners and Laggards

This ranking view is useful for summarizing sector leadership in a way that non-technical audiences can read quickly.
"""
        ),
        nbf.v4.new_code_cell(
            """plot_yearly_winners(bundle, root / "figures" / "yearly_winners_laggards.png")
display(Image(filename=str(root / "figures" / "yearly_winners_laggards.png")))
display(bundle.yearly_rankings.sort_values(["Year", "rank"]).head(15))
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 7. Key Findings

The statements below are generated from the analysis outputs rather than written by hand.
"""
        ),
        nbf.v4.new_code_cell(
            """for idx, finding in enumerate(bundle.findings, start=1):
    print(f"{idx}. {finding}")
"""
        ),
        nbf.v4.new_markdown_cell(
            """## 8. Conclusion

The evidence supports a rotation narrative:

- leadership changed significantly across the pandemic, the 2022 hiking cycle, and the later recovery;
- sector choice materially affected both return and risk outcomes;
- a diversified or rotation-aware allocation framework is more defensible than treating all sectors as interchangeable.
"""
        ),
    ]

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    }
    return nb


def main() -> None:
    root = ROOT
    notebook_path = root / "notebook.ipynb"
    nb = build_notebook()
    nbf.write(nb, notebook_path)


if __name__ == "__main__":
    main()
