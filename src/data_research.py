# src/data_research.py
from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main() -> int:
    path = RAW_DIR / "queue.csv"
    if not path.exists():
        print("queue.csv not found in data/raw/. Run data_load first.")
        return 2

    df = pd.read_csv(path)

    # TODO: після того як подивишся df.columns, вкажи правильні назви полів:
    # Наприклад: datetime_col = "created_at" / "timestamp" / "date" ...
    # point_col = "checkpoint" / "pp_name" ...
    print("COLUMNS:", list(df.columns))
    print(df.head(5).to_string(index=False))

    # Мінімальна EDA-статистика:
    stats_path = REPORT_DIR / "eda_basic_queue.txt"
    with stats_path.open("w", encoding="utf-8") as w:
        w.write("BASIC INFO\n")
        w.write(str(df.describe(include="all").transpose()))
        w.write("\n")

    print("Saved:", stats_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())