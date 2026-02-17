# src/visualization.py
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RAW_DIR = Path("data/raw")
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def main() -> int:
    path = RAW_DIR / "queue.csv"
    if not path.exists():
        print("queue.csv not found in data/raw/. Run data_load first.")
        return 2

    df = pd.read_csv(path)
    print("COLUMNS:", list(df.columns))

    # TODO: постав правильну колонку з датою/часом
    # dt_col = "..."
    # df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")

    # Приклад: якщо є datetime — можна побудувати кількість записів по днях:
    # daily = df.set_index(dt_col).resample("D").size()
    # plt.figure()
    # daily.plot()
    # plt.title("Записи черги по днях")
    # plt.tight_layout()
    # out = FIG_DIR / "queue_daily.png"
    # plt.savefig(out, dpi=150)

    # Поки просто збережемо “заглушку” графіка розміру датасету:
    plt.figure()
    plt.bar(["rows", "cols"], [df.shape[0], df.shape[1]])
    plt.title("Розмір датасету queue.csv")
    plt.tight_layout()
    out = FIG_DIR / "dataset_size.png"
    plt.savefig(out, dpi=150)
    print("Saved:", out)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())