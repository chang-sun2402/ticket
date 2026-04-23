# ACC102 Mini Assignment · Project Plan

> **Track**: Track 2 – GitHub Data Analysis Project
> **Deadline**: 27 April 2026, 23:59 (LMO submission)
> **Target Score**: 80+ core + Bonus (up to +10)

---

## 1. Project Overview

| Item | Description |
|------|-------------|
| Title | US Equity Sector Rotation Analysis |
| Target Users | Individual investors seeking to adjust sector allocations across macroeconomic cycles; Finance/Economics students learning about sector-level market behaviour |
| Core Question | Do different US market sectors (Technology, Healthcare, Energy, Financials, Consumer Discretionary) exhibit rotation patterns over time? Which sectors outperform under specific macroeconomic conditions? |
| Data Source | Yahoo Finance via the `yfinance` Python library (free, no registration required, widely used in academic and practitioner contexts) |
| Analysis Period | January 2020 – December 2024 (covering COVID-19 crash, monetary tightening, and recovery cycles) |
| ETFs Used | XLK (Technology), XLV (Healthcare), XLE (Energy), XLF (Financials), XLY (Consumer Discretionary) — all are SPDR sector ETFs with high liquidity and long histories |

---

## 2. Rationale for Choosing Track 2

- **Analytical depth suits the dataset**: Sector rotation is a multi-dimensional problem that naturally requires data acquisition, cleaning, transformation, visualisation, and comparative analysis — aligning well with the 30-mark Python Implementation criterion.
- **GitHub as a professional portfolio**: Publishing on GitHub creates a reusable, publicly accessible portfolio piece that demonstrates both analytical and communication skills.
- **Reproducibility and transparency**: A well-structured GitHub repository with a clear README, notebook, and requirements file makes the analytical workflow fully reproducible — a hallmark of responsible data practice.
- **Clear user-facing output**: The analysis produces actionable sector-level insights that can be directly communicated to the target audience, supporting the Product Design criterion.
- **Bonus opportunity**: Track 2 offers up to 10 bonus marks for GitHub quality, incentivising clean code structure and thorough documentation.

---

## 3. Data Ethics & Legal Compliance

- **Lawfulness**: Yahoo Finance data accessed via `yfinance` is publicly available market data. Its use for educational analysis is consistent with Yahoo's Terms of Service for non-commercial, academic purposes.
- **Reliability**: SPDR sector ETFs (XLK, XLV, XLE, XLF, XLY) are among the most liquid and widely tracked ETFs, ensuring data quality and representativeness.
- **Acknowledgement**: The data source (Yahoo Finance) and the access date will be clearly stated in both the notebook and the README, as required by the assignment.
- **Limitations**: End-of-day adjusted closing prices do not capture intraday volatility or after-hours movements. This limitation will be explicitly noted in the analysis and reflection report.

---

## 4. Submission Checklist

### Required Materials (via LMO)
- [ ] `notebook.ipynb` — Full Python analysis notebook (**primary deliverable**)
- [ ] Reflection report (500–800 words, including AI disclosure)
- [ ] GitHub repository link
- [ ] Mediasite demo video link (1–3 minutes)

### Optional Bonus Materials
- [ ] `streamlit_app.py` or lightweight interactive demo (**supplementary only, does not replace notebook**)

### GitHub Repository Must Include
- [ ] `README.md`
- [ ] `notebook.ipynb` (primary analysis and marking basis)
- [ ] `requirements.txt`
- [ ] `data/` (data files if <25 MB; otherwise document source in README)
- [ ] `figures/` (saved charts — optional but adds value)

### GitHub Repository Optional Supplements
- [ ] `streamlit_app.py` (for interactive demo, not required)
- [ ] `app_screenshots/` (if Streamlit is used, include interface screenshots)

---

## 5. Python Analysis Steps (Notebook Structure)

> Adopt a **notebook-first, Streamlit-as-supplement** delivery strategy. The notebook is the primary deliverable for marking; Streamlit may be added for enhanced presentation.

### Step 1 · Data Acquisition
- Download daily adjusted closing prices for XLK, XLV, XLE, XLF, XLY from Yahoo Finance using `yfinance` for the period Jan 2020 – Dec 2024
- **Rationale**: `yfinance` provides free, programmatic access to Yahoo Finance data with no API key required. Adjusted close prices account for dividends and stock splits, ensuring return calculations are accurate.
- Record the data source (Yahoo Finance) and access date in a markdown cell at the top of the notebook (assignment requirement)
- Print dataset shape, date range, and basic statistics to verify download integrity

### Step 2 · Data Cleaning & Preparation
- Check for missing values using `df.isnull().sum()`; handle with `dropna()` or forward-fill (`ffill`) depending on the pattern
  - **Rationale**: ETF data is generally clean, but missing values may occur on market holidays. `dropna()` is preferred when gaps are few and random; `ffill` is used when continuity is needed for rolling calculations.
- Calculate daily returns using `df.pct_change()`
- Calculate monthly returns using `df.resample('ME').last().pct_change()`
- Calculate quarterly returns using `df.resample('QE').last().pct_change()`
  - **Rationale**: Multiple return frequencies allow the analysis to capture both short-term and medium-term rotation patterns.

### Step 3 · Analysis (Core — must be thorough and well-reasoned)

| Analysis | Implementation | Rationale | Marks Alignment |
|----------|---------------|-----------|-----------------|
| Cumulative return comparison | Line chart (`matplotlib` / `plotly`) | Cumulative returns show the total wealth trajectory per sector — the most intuitive metric for investors | Visualisation basics |
| Annual & quarterly return heatmaps | `seaborn.heatmap` | Heatmaps enable rapid visual identification of which sectors outperform/underperform in each period — the core of rotation analysis | Highlight visualisation |
| Cross-sector correlation matrix | `df.corr()` + `seaborn.heatmap` | Correlation reveals co-movement patterns; low-correlation sectors offer diversification benefits — directly relevant to investor decisions | Relationship analysis |
| 30-day rolling volatility | `df.rolling(30).std()` | 30 days balances responsiveness and smoothness; shorter windows (e.g., 10d) are too noisy, longer windows (e.g., 60d) lag too much | Risk dimension |
| Yearly best/worst sector ranking | `groupby` year + sort | Annual rankings summarise rotation patterns concisely and support actionable conclusions | Insight synthesis |

### Step 4 · Conclusions & Insights
- Summarise 3–5 actionable findings with specific numbers
- Example: "In 2022, the Energy sector (XLE) rose XX% while Technology (XLK) fell XX%, aligning with the Federal Reserve's tightening cycle — a pattern consistent with historical sector rotation under rising-rate environments."
- Each finding should connect to the target user's decision-making context

---

## 6. Environment Configuration

| Item | Specification |
|------|--------------|
| Python version | 3.10+ |
| Key dependencies | `yfinance`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly` |
| Environment file | `requirements.txt` listing all packages with pinned versions (e.g., `yfinance==0.2.36`) |
| Optional | `environment.yml` for conda users; `streamlit` if the supplementary app is included |
| Run instructions | The README will include: (1) `pip install -r requirements.txt`; (2) open `notebook.ipynb` in Jupyter; (3) Run All cells |

---

## 7. README Structure

> If Streamlit is provided, clearly label it as an **optional demo** in the README. Do NOT let the marker assume it replaces the notebook.

```
# Project Title (English only)

> Demo Video: [Mediasite link] (placed near the top for immediate visibility)

## 1. Problem & User
## 2. Data (source + access date + key fields)
## 3. Methods (Python analysis steps — brief overview)
## 4. Key Findings (3–5 numbered conclusions)
## 5. How to Run (environment setup + execution)
## 6. Limitations & Next Steps
```

> ⚠️ The demo video link must be placed near the top of the README so the marker can find it immediately.

---

## 8. Demo Video Plan (1–3 minutes)

| Time | Content |
|------|---------|
| 0–20s | Introduce the problem background and target users |
| 20–40s | Briefly describe the data source and structure |
| 40–120s | **Run notebook code cells live**, showing key analysis steps (not screenshots — actual execution) |
| 120–160s | Present main charts and explain findings (if Streamlit is available, briefly show the interactive interface) |
| 160–180s | Show repository structure (README location, notebook location; if app exists, clarify it is supplementary) |

> ⚠️ Video must be uploaded to **Mediasite** (not YouTube / Bilibili / other platforms) — this is a Track 2 requirement.
> ⚠️ Video narration or subtitles must be in English (assignment requirement). Text-to-speech tools (e.g., MiniMax) are acceptable.

---

## 9. Reflection Report Outline (500–800 words)

1. State the analytical problem and intended user/audience
2. Describe the dataset and explain why it was selected
3. Explain the Python methods used
4. Summarise the main insights or outputs produced
5. Evaluate limitations, reliability issues, and possible improvements (e.g., data timeliness, sample selection bias, only US market covered)
6. Briefly explain your own contribution, decisions, and what you learned
7. **AI Disclosure** (placed at the end, using the format below)

### AI Disclosure Format

For each AI tool used, provide the following:

```
AI Tool: [tool name]
Model/Version: [e.g., GPT-4o, Claude 3.5 Sonnet]
Access Date: [YYYY-MM-DD]
Purpose: [specific use, e.g., "assisted with data cleaning code", "helped refine chart labels"]
```

---

## 10. Common Pitfalls — Self-Check List

- [ ] Notebook uses absolute file paths → change to relative paths
- [ ] Data source does not include an access date
- [ ] README missing the demo video link
- [ ] Video only shows chart results without running code live
- [ ] Reflection report missing the AI disclosure
- [ ] Submitted only links on LMO without attaching the notebook and reflection report
- [ ] **All materials not in English (notebook, README, reflection report, video narration must be in English)**
- [ ] `requirements.txt` does not match actual dependencies used
- [ ] Notebook or README missing setup/run instructions

---

## 11. Project Timeline

| Date | Milestone |
|------|-----------|
| Apr 22 | Finalise project plan; set up GitHub repository structure |
| Apr 23 | Complete data acquisition and cleaning (Steps 1–2 in notebook) |
| Apr 24 | Complete core analysis and visualisation (Step 3 in notebook) |
| Apr 25 | Write conclusions; polish notebook with markdown narrative; generate saved figures |
| Apr 26 | Write README; record and upload demo video to Mediasite; write reflection report |
| Apr 27 | Final self-check against checklist; submit all materials via LMO before 23:59 |

---

## 12. Estimated Score

| Criterion | Max | Conservative Estimate |
|-----------|-----|-----------------------|
| Problem Definition and Data Relevance | 20 | 16–18 |
| Python Implementation and Technical Execution | 30 | 23–26 |
| Analysis, Insight, and Interpretation | 20 | 15–17 |
| Product Design, Communication, and User Focus | 20 | 15–17 |
| Reflection, Limitations, and Professional Practice | 10 | 7–9 |
| **Core Total** | **100** | **~76–87** |
| Bonus (GitHub quality) | +10 | +5–8 |

> Estimates are deliberately conservative. Actual scores depend on execution quality, depth of analysis, and how well the final deliverables communicate value to the target user.

---

*Document version: v2.0 · Updated: 2026-04-22*
