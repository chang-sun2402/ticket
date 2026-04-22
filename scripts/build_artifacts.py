from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sector_rotation_analysis import (  # noqa: E402
    ACCESS_DATE,
    END_DATE,
    START_DATE,
    TICKER_MAP,
    build_analysis,
    ensure_output_dirs,
)


def main() -> None:
    root = ROOT
    output_dirs = ensure_output_dirs(root)
    bundle = build_analysis(root)

    summary = {
        "title": "US Sector Rotation Analysis",
        "subtitle": "Track 2 GitHub Data Analysis Project",
        "tickers": TICKER_MAP,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "access_date": ACCESS_DATE,
        "key_findings": bundle.findings,
        "top_sector": bundle.summary_metrics.index[0],
        "top_sector_total_return": float(bundle.summary_metrics.iloc[0]["Total Return"]),
        "lowest_sector": bundle.summary_metrics.index[-1],
        "lowest_sector_total_return": float(bundle.summary_metrics.iloc[-1]["Total Return"]),
        "best_2022_sector": bundle.annual_returns.loc[2022].idxmax(),
        "best_2022_return": float(bundle.annual_returns.loc[2022].max()),
        "best_2023_sector": bundle.annual_returns.loc[2023].idxmax(),
        "best_2023_return": float(bundle.annual_returns.loc[2023].max()),
    }
    (output_dirs["reports"] / "analysis_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
