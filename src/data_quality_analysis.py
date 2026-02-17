# src/data_quality_analysis.py
from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def quality_report(df: pd.DataFrame) -> dict:
    report = {}
    report["rows"] = int(df.shape[0])
    report["cols"] = int(df.shape[1])
    report["missing_by_col"] = df.isna().sum().sort_values(ascending=False).to_dict()
    report["duplicate_rows"] = int(df.duplicated().sum())
    return report

def main() -> int:
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        print("No CSV files in data/raw/. Run data_load first.")
        return 2

    for f in files:
        df = pd.read_csv(f)
        rep = quality_report(df)

        out = REPORT_DIR / f"quality_{f.stem}.txt"
        with out.open("w", encoding="utf-8") as w:
            w.write(f"FILE: {f}\n")
            w.write(f"ROWS: {rep['rows']}\nCOLS: {rep['cols']}\n")
            w.write(f"DUPLICATES: {rep['duplicate_rows']}\n\n")
            w.write("MISSING BY COLUMN:\n")
            for k, v in rep["missing_by_col"].items():
                w.write(f"- {k}: {v}\n")

        print("Saved:", out)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())