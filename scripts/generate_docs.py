from __future__ import annotations

import json
from pathlib import Path


def load_summary(root: Path) -> dict:
    return json.loads((root / "reports" / "analysis_summary.json").read_text(encoding="utf-8"))


def build_readme(summary: dict) -> str:
    findings = "\n".join(f"- {item}" for item in summary["key_findings"])
    ticker_lines = "\n".join(
        f"| `{ticker}` | {sector} |"
        for ticker, sector in summary["tickers"].items()
    )

    return f"""# 板块轮动分析 | Sector Rotation Analysis

Track 2 GitHub Data Analysis Project focused on whether major equity sectors rotate across different macro regimes.

**Demo Video (Mediasite):** `Replace this placeholder with your final Mediasite link before submission`

## Snapshot

| Metric | Result |
|---|---|
| Best full-period sector | **{summary["top_sector"]}** ({summary["top_sector_total_return"]:.1%} total return) |
| Weakest full-period sector | **{summary["lowest_sector"]}** ({summary["lowest_sector_total_return"]:.1%} total return) |
| 2022 defensive winner | **{summary["best_2022_sector"]}** ({summary["best_2022_return"]:.1%}) |
| 2023 rebound leader | **{summary["best_2023_sector"]}** ({summary["best_2023_return"]:.1%}) |

<p align="center">
  <img src="figures/cumulative_returns.png" alt="Cumulative returns chart" width="48%" />
  <img src="figures/annual_returns_heatmap.png" alt="Annual returns heatmap" width="48%" />
</p>

## 1. Problem & User

This project asks whether sector performance follows a rotation pattern across the pandemic shock, the 2022 rate-hike cycle, and the 2023-2024 recovery. The target users are individual investors and finance/economics students who want a practical, visual way to understand cross-sector leadership.

## 2. Data

- Source: Yahoo Finance via the `yfinance` Python package
- Access date: {summary["access_date"]}
- Analysis window: {summary["start_date"]} to {summary["end_date"]}
- Frequency: daily prices, transformed into daily / monthly / quarterly returns

| ETF | Sector |
|---|---|
{ticker_lines}

Generated datasets are stored in `data/`, including daily prices, daily returns, monthly returns, annual returns, rolling volatility, correlation matrix, and yearly rankings.

## 3. Methods

- Download adjusted close prices for five representative US sector ETFs
- Clean missing values with forward fill and common-date alignment
- Compute daily returns with `pct_change()` and monthly returns with `resample('ME')`
- Compare cumulative returns across sectors
- Build annual and quarterly return heatmaps
- Measure cross-sector correlation
- Estimate 30-day rolling annualized volatility
- Rank the strongest and weakest sector each year

## 4. Key Findings

{findings}

## 5. Visual Preview

<p align="center">
  <img src="figures/quarterly_returns_heatmap.png" alt="Quarterly returns heatmap" width="48%" />
  <img src="figures/correlation_heatmap.png" alt="Correlation heatmap" width="48%" />
</p>

<p align="center">
  <img src="figures/rolling_volatility.png" alt="Rolling volatility chart" width="48%" />
  <img src="figures/yearly_winners_laggards.png" alt="Yearly winners and laggards" width="48%" />
</p>

## 6. How to Run

### Conda environment

```bash
conda env create -f environment.yml
conda activate acc102_track2
python scripts/build_artifacts.py
python scripts/generate_notebook.py
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb
```

### Optional Streamlit demo

```bash
streamlit run streamlit_app.py
```

## 7. Repository Structure

```text
.
|-- ACC102_Track2_ProjectPlan.md
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

## 8. Limitations & Next Steps

- ETF proxies simplify sector exposure and do not capture every stock in each sector
- Yahoo Finance is convenient and free, but institutional datasets would offer cleaner fundamentals and intraday detail
- Macro interpretation is suggestive rather than causal; adding inflation, rates, and oil variables would deepen the explanation
- A next step would be a factor-based rotation model or a simple regime classifier for sector allocation
"""


def build_reflection(summary: dict) -> str:
    return f"""# ACC102 Track 2 反思报告

本项目围绕“板块轮动分析”展开，目标用户是个人投资者和金融、经济学学生。我希望回答的问题是：在不同宏观环境下，科技、消费、能源、医疗和金融等板块是否存在相对明确的轮动规律，以及这种轮动是否能够帮助用户更好地理解市场风格切换。相比直接讨论单只股票，行业 ETF 更适合作为教学和分析入口，因为它们能够降低个股噪声，让用户把注意力集中在板块层面的相对强弱变化上。

我选择 Yahoo Finance 和 `yfinance` 作为数据来源，主要原因是它免费、获取方便、复现成本低，适合课程作业在 GitHub 上完整展示。本项目使用了 2020 年 1 月到 2024 年 12 月的日度价格数据，这一时间段覆盖了疫情冲击、经济复苏、激进加息以及 AI 驱动的成长反弹等多个阶段，因此更容易观察风格轮动。为了让分析路径清晰，我首先下载五只代表性美股行业 ETF 的调整后收盘价，然后进行了缺失值处理和时间对齐，再计算日收益率、月度收益率和季度收益率，作为后续分析的基础。

在 Python 方法上，我使用了 `pandas` 进行数据清洗和重采样，使用 `pct_change()` 计算收益率，使用 `groupby`、排序和透视逻辑完成年度强弱排名，使用 `matplotlib` 与 `seaborn` 输出累计收益曲线、年度与季度热力图、相关性矩阵以及 30 日滚动波动率图。通过这些图表，我不仅能比较长期回报，也能从风险和联动性的角度理解不同板块在市场压力下的表现差异。最终分析结果显示，板块领导权会随着宏观环境变化而明显切换，支持“板块轮动”这一核心命题。

项目最重要的收获是，我比以前更清楚地理解了“结论需要从结构化分析流程中长出来”，而不是先有观点再挑图表支持。例如，2022 年能源板块与其他板块出现显著背离，而 2023 年成长板块重新领先，这种变化只有在统一的数据口径和连续时间框架里才容易被看见。另外，我也意识到可视化设计会直接影响商业沟通效果。同样的数据，如果只是简单输出表格，很难让非技术用户快速抓住重点；而经过配色、标题和结构优化后的图表，会更适合在视频展示和 GitHub README 中传达洞察。

当然，这个项目也有局限。第一，ETF 只是板块代理变量，无法完全代表全部成分股特征。第二，Yahoo Finance 数据更适合教学和快速分析，不等同于专业金融终端。第三，本项目主要做描述性分析，尚未建立因果模型或预测模型，因此对“为什么会轮动”的解释仍然偏经验性。未来如果继续扩展，我希望加入利率、通胀、油价等宏观变量，并尝试一个简单的板块轮动策略回测或宏观情景分类器。

本项目的个人贡献主要包括：确定研究问题、设计分析框架、编写 Python 数据处理与可视化代码、生成 notebook 和 GitHub 文档结构，并将结果整理为可复现的仓库形式。整个过程中，我提升了对金融时间序列分析、项目结构化交付以及面向评分标准组织作品的能力。

## AI 声明

- Tool: OpenAI Codex / GPT-5 系列编码助手
- Access date: 2026-04-21
- Usage: 协助梳理项目结构、生成部分 Python 代码、撰写 README 与反思报告初稿、优化表达与可视化呈现
- Final responsibility: 数据验证、结果检查、最终提交内容确认由本人完成
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    summary = load_summary(root)
    (root / "README.md").write_text(build_readme(summary), encoding="utf-8")
    (root / "reflection_report.md").write_text(build_reflection(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
