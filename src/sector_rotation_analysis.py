from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf


TICKER_MAP = {
    "XLK": "Technology",
    "XLY": "Consumer Discretionary",
    "XLE": "Energy",
    "XLV": "Health Care",
    "XLF": "Financials",
}

FALLBACK_TICKERS = {
    "XLE": "VDE",
}

START_DATE = "2020-01-01"
END_DATE = "2024-12-31"
ACCESS_DATE = "2026-04-21"

FIGURE_STYLE = {
    "axes.facecolor": "#fbf7ef",
    "figure.facecolor": "#f4efe4",
    "axes.edgecolor": "#40352c",
    "axes.labelcolor": "#2e251f",
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "grid.color": "#d9c9a8",
    "text.color": "#2e251f",
    "xtick.color": "#2e251f",
    "ytick.color": "#2e251f",
    "font.family": "DejaVu Sans",
}

PALETTE = {
    "Technology": "#0b6e4f",
    "Consumer Discretionary": "#d97706",
    "Energy": "#b42318",
    "Health Care": "#2667ff",
    "Financials": "#6b21a8",
}


@dataclass
class AnalysisBundle:
    prices: pd.DataFrame
    daily_returns: pd.DataFrame
    monthly_returns: pd.DataFrame
    quarterly_returns: pd.DataFrame
    cumulative_returns: pd.DataFrame
    rolling_volatility: pd.DataFrame
    annual_returns: pd.DataFrame
    correlation_matrix: pd.DataFrame
    yearly_rankings: pd.DataFrame
    summary_metrics: pd.DataFrame
    findings: list[str]


def ensure_output_dirs(root: Path) -> dict[str, Path]:
    data_dir = root / "data"
    figures_dir = root / "figures"
    reports_dir = root / "reports"
    for directory in (data_dir, figures_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)
    return {"data": data_dir, "figures": figures_dir, "reports": reports_dir}


def configure_plot_style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(FIGURE_STYLE)


def download_sector_prices(
    tickers: Iterable[str] | None = None,
    start: str = START_DATE,
    end: str = END_DATE,
) -> pd.DataFrame:
    tickers = list(tickers or TICKER_MAP.keys())
    end = "2025-01-01" if end == END_DATE else end
    series_map: dict[str, pd.Series] = {}

    for ticker in tickers:
        candidates = [ticker]
        if ticker in FALLBACK_TICKERS:
            candidates.append(FALLBACK_TICKERS[ticker])

        sector_name = TICKER_MAP[ticker]
        sector_series = None
        for candidate in candidates:
            for _ in range(3):
                raw = yf.download(
                    tickers=candidate,
                    start=start,
                    end=end,
                    auto_adjust=True,
                    progress=False,
                    threads=False,
                )
                if raw.empty:
                    time.sleep(1)
                    continue

                if isinstance(raw.columns, pd.MultiIndex):
                    close_series = raw["Close"][candidate].copy()
                else:
                    close_series = raw["Close"].copy()

                close_series = close_series.dropna()
                if not close_series.empty:
                    sector_series = close_series.rename(sector_name)
                    break
                time.sleep(1)
            if sector_series is not None:
                break

        if sector_series is None:
            raise ValueError(f"No price data returned for {ticker} or its fallback tickers.")
        series_map[sector_name] = sector_series

    prices = pd.concat(series_map.values(), axis=1).sort_index()
    prices.index = pd.to_datetime(prices.index)
    prices = prices.ffill().dropna()
    return prices


def compute_analysis(prices: pd.DataFrame) -> AnalysisBundle:
    daily_returns = prices.pct_change().dropna()
    monthly_prices = prices.resample("ME").last()
    monthly_returns = monthly_prices.pct_change().dropna()
    quarterly_prices = prices.resample("QE").last()
    quarterly_returns = quarterly_prices.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    rolling_volatility = daily_returns.rolling(30).std() * np.sqrt(252)
    annual_returns = monthly_returns.groupby(monthly_returns.index.year).apply(
        lambda frame: (1 + frame).prod() - 1
    )
    annual_returns.index.name = "Year"
    annual_returns.columns.name = None

    correlation_matrix = daily_returns.corr()
    yearly_rankings = (
        annual_returns.stack()
        .rename("return")
        .reset_index()
        .rename(columns={"level_1": "Sector"})
        .sort_values(["Year", "return"], ascending=[True, False])
    )
    yearly_rankings["rank"] = yearly_rankings.groupby("Year")["return"].rank(
        ascending=False, method="first"
    )

    summary_metrics = pd.DataFrame(
        {
            "CAGR": ((prices.iloc[-1] / prices.iloc[0]) ** (1 / 5)) - 1,
            "Total Return": (prices.iloc[-1] / prices.iloc[0]) - 1,
            "Annualized Volatility": daily_returns.std() * np.sqrt(252),
            "Best Month": monthly_returns.max(),
            "Worst Month": monthly_returns.min(),
        }
    ).sort_values("Total Return", ascending=False)

    findings = build_findings(annual_returns, summary_metrics, correlation_matrix)

    return AnalysisBundle(
        prices=prices,
        daily_returns=daily_returns,
        monthly_returns=monthly_returns,
        quarterly_returns=quarterly_returns,
        cumulative_returns=cumulative_returns,
        rolling_volatility=rolling_volatility,
        annual_returns=annual_returns,
        correlation_matrix=correlation_matrix,
        yearly_rankings=yearly_rankings,
        summary_metrics=summary_metrics,
        findings=findings,
    )


def build_findings(
    annual_returns: pd.DataFrame,
    summary_metrics: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
) -> list[str]:
    strongest_2022 = annual_returns.loc[2022].idxmax()
    strongest_2022_value = annual_returns.loc[2022].max()
    weakest_2022 = annual_returns.loc[2022].idxmin()
    weakest_2022_value = annual_returns.loc[2022].min()

    strongest_2023 = annual_returns.loc[2023].idxmax()
    strongest_2023_value = annual_returns.loc[2023].max()

    leader = summary_metrics.index[0]
    leader_return = summary_metrics.iloc[0]["Total Return"]
    laggard = summary_metrics.index[-1]
    laggard_return = summary_metrics.iloc[-1]["Total Return"]

    corr_pairs = (
        correlation_matrix.where(~np.eye(len(correlation_matrix), dtype=bool))
        .stack()
        .sort_values(ascending=False)
    )
    top_pair = corr_pairs.index[0]
    top_pair_value = corr_pairs.iloc[0]

    return [
        (
            f"In 2022, {strongest_2022} was the only clear defensive winner, returning "
            f"{strongest_2022_value:.1%}, while {weakest_2022} dropped {abs(weakest_2022_value):.1%}."
        ),
        (
            f"The 2023 rebound was led by {strongest_2023}, which gained {strongest_2023_value:.1%} "
            "as growth assets recovered."
        ),
        (
            f"Across the full 2020-2024 window, {leader} delivered the highest total return at {leader_return:.1%}, "
            f"while {laggard} lagged at {laggard_return:.1%}."
        ),
        (
            f"The tightest daily co-movement came from {top_pair[0]} and {top_pair[1]}, "
            f"with a correlation of {top_pair_value:.2f}, indicating strong cyclical overlap."
        ),
        (
            "Sector leadership changed materially between the pandemic shock, the 2022 hiking cycle, "
            "and the 2023-2024 recovery, which supports a rotation-based allocation lens."
        ),
    ]


def save_tables(bundle: AnalysisBundle, output_dirs: dict[str, Path]) -> None:
    output_dirs["data"].mkdir(exist_ok=True)
    bundle.prices.to_csv(output_dirs["data"] / "sector_prices_daily.csv")
    bundle.daily_returns.to_csv(output_dirs["data"] / "daily_returns.csv")
    bundle.monthly_returns.to_csv(output_dirs["data"] / "monthly_returns.csv")
    bundle.quarterly_returns.to_csv(output_dirs["data"] / "quarterly_returns.csv")
    bundle.annual_returns.to_csv(output_dirs["data"] / "annual_returns.csv")
    bundle.rolling_volatility.to_csv(output_dirs["data"] / "rolling_volatility_30d.csv")
    bundle.correlation_matrix.to_csv(output_dirs["data"] / "correlation_matrix.csv")
    bundle.yearly_rankings.to_csv(output_dirs["data"] / "yearly_rankings.csv", index=False)
    bundle.summary_metrics.to_csv(output_dirs["reports"] / "summary_metrics.csv")
    (output_dirs["reports"] / "key_findings.md").write_text(
        "\n".join(f"- {finding}" for finding in bundle.findings),
        encoding="utf-8",
    )


def _format_percent_axis(ax: plt.Axes) -> None:
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f"{value:.0%}"))


def plot_cumulative_returns(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    for sector in bundle.cumulative_returns.columns:
        ax.plot(
            bundle.cumulative_returns.index,
            bundle.cumulative_returns[sector],
            label=sector,
            linewidth=2.5,
            color=PALETTE[sector],
        )
    ax.set_title("Cumulative Sector Returns (2020-2024)")
    ax.set_ylabel("Cumulative Return")
    ax.legend(frameon=False, ncols=3)
    _format_percent_axis(ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_annual_heatmap(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(10, 4.8))
    sns.heatmap(
        bundle.annual_returns.T * 100,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn",
        center=0,
        linewidths=0.6,
        cbar_kws={"label": "Return (%)"},
        ax=ax,
    )
    ax.set_title("Annual Sector Returns Heatmap")
    ax.set_xlabel("Year")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_quarterly_heatmap(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    quarter_labels = bundle.quarterly_returns.index.to_period("Q").astype(str)
    heatmap_df = bundle.quarterly_returns.copy()
    heatmap_df.index = quarter_labels
    fig, ax = plt.subplots(figsize=(14, 5.5))
    sns.heatmap(
        heatmap_df.T * 100,
        cmap="Spectral",
        center=0,
        linewidths=0.4,
        cbar_kws={"label": "Return (%)"},
        ax=ax,
    )
    ax.set_title("Quarterly Sector Rotation Heatmap")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_correlation_heatmap(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(7.5, 6))
    sns.heatmap(
        bundle.correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="crest",
        vmin=0,
        vmax=1,
        linewidths=0.6,
        square=True,
        ax=ax,
    )
    ax.set_title("Daily Return Correlation Across Sectors")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_rolling_volatility(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    for sector in bundle.rolling_volatility.columns:
        ax.plot(
            bundle.rolling_volatility.index,
            bundle.rolling_volatility[sector],
            label=sector,
            linewidth=2.0,
            color=PALETTE[sector],
        )
    ax.set_title("30-Day Rolling Annualized Volatility")
    ax.set_ylabel("Volatility")
    ax.legend(frameon=False, ncols=3)
    _format_percent_axis(ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_yearly_winners(bundle: AnalysisBundle, output_path: Path) -> None:
    configure_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    winners = bundle.yearly_rankings.loc[
        bundle.yearly_rankings.groupby("Year")["rank"].idxmin()
    ].copy()
    losers = bundle.yearly_rankings.loc[
        bundle.yearly_rankings.groupby("Year")["rank"].idxmax()
    ].copy()

    sns.barplot(
        data=winners,
        x="return",
        y="Year",
        hue="Sector",
        dodge=False,
        palette=PALETTE,
        ax=axes[0],
    )
    axes[0].set_title("Yearly Winners")
    axes[0].set_xlabel("Return")
    axes[0].set_ylabel("")
    axes[0].legend_.remove()
    _format_percent_axis(axes[0])

    sns.barplot(
        data=losers,
        x="return",
        y="Year",
        hue="Sector",
        dodge=False,
        palette=PALETTE,
        ax=axes[1],
    )
    axes[1].set_title("Yearly Laggards")
    axes[1].set_xlabel("Return")
    axes[1].set_ylabel("")
    axes[1].legend(frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left")
    _format_percent_axis(axes[1])

    fig.tight_layout()
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def generate_figures(bundle: AnalysisBundle, output_dirs: dict[str, Path]) -> None:
    plot_cumulative_returns(bundle, output_dirs["figures"] / "cumulative_returns.png")
    plot_annual_heatmap(bundle, output_dirs["figures"] / "annual_returns_heatmap.png")
    plot_quarterly_heatmap(bundle, output_dirs["figures"] / "quarterly_returns_heatmap.png")
    plot_correlation_heatmap(bundle, output_dirs["figures"] / "correlation_heatmap.png")
    plot_rolling_volatility(bundle, output_dirs["figures"] / "rolling_volatility.png")
    plot_yearly_winners(bundle, output_dirs["figures"] / "yearly_winners_laggards.png")


def build_analysis(root: Path) -> AnalysisBundle:
    output_dirs = ensure_output_dirs(root)
    prices = download_sector_prices()
    bundle = compute_analysis(prices)
    save_tables(bundle, output_dirs)
    generate_figures(bundle, output_dirs)
    return bundle
