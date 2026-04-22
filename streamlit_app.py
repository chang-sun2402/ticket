from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIGURES_DIR = ROOT / "figures"
REPORTS_DIR = ROOT / "reports"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    summary_metrics = pd.read_csv(REPORTS_DIR / "summary_metrics.csv", index_col=0)
    annual_returns = pd.read_csv(DATA_DIR / "annual_returns.csv", index_col=0)
    findings = (REPORTS_DIR / "key_findings.md").read_text(encoding="utf-8").splitlines()
    findings = [line.removeprefix("- ").strip() for line in findings if line.strip()]
    return summary_metrics, annual_returns, findings


st.set_page_config(
    page_title="Sector Rotation Dashboard",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(11, 110, 79, 0.12), transparent 30%),
            radial-gradient(circle at top right, rgba(217, 119, 6, 0.12), transparent 35%),
            linear-gradient(180deg, #f5efe4 0%, #fcfaf5 100%);
    }
    .hero {
        padding: 1.4rem 1.6rem;
        border: 1px solid rgba(64, 53, 44, 0.15);
        border-radius: 24px;
        background: rgba(255, 250, 240, 0.72);
        backdrop-filter: blur(8px);
        margin-bottom: 1rem;
    }
    .metric-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(64, 53, 44, 0.12);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.2rem;">Sector Rotation Analysis</h1>
        <p style="margin:0;color:#524438;">
            A visual summary of how Technology, Consumer, Energy, Health Care, and Financials rotated from 2020 to 2024.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

summary_metrics, annual_returns, findings = load_data()
leader = summary_metrics.index[0]
laggard = summary_metrics.index[-1]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Top Total Return", leader, f"{summary_metrics.iloc[0]['Total Return']:.1%}")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Lowest Total Return", laggard, f"{summary_metrics.iloc[-1]['Total Return']:.1%}")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    best_year = annual_returns.max(axis=1).idxmax()
    best_return = annual_returns.max(axis=1).max()
    st.metric("Best Sector-Year", str(best_year), f"{best_return:.1%}")
    st.markdown("</div>", unsafe_allow_html=True)

st.subheader("Key Findings")
for finding in findings:
    st.write(f"- {finding}")

st.subheader("Summary Metrics")
st.dataframe(summary_metrics.style.format("{:.1%}"), use_container_width=True)

st.subheader("Figure Gallery")
figure_cols = st.columns(2)
figure_paths = [
    FIGURES_DIR / "cumulative_returns.png",
    FIGURES_DIR / "annual_returns_heatmap.png",
    FIGURES_DIR / "quarterly_returns_heatmap.png",
    FIGURES_DIR / "correlation_heatmap.png",
    FIGURES_DIR / "rolling_volatility.png",
    FIGURES_DIR / "yearly_winners_laggards.png",
]
for idx, figure_path in enumerate(figure_paths):
    with figure_cols[idx % 2]:
        st.image(str(figure_path), use_container_width=True)
