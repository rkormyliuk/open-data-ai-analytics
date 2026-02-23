from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RAW_FILE = Path("data/raw/salary_by_region.csv")
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def read_csv_auto_sep(path: Path) -> pd.DataFrame:
    first_line = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    sep = "," if first_line.count(",") >= first_line.count(";") else ";"
    return pd.read_csv(path, encoding="utf-8", sep=sep, engine="python", dtype=str, on_bad_lines="skip")


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={df.columns[0]: "region"}).copy()
    df["region"] = df["region"].astype(str).str.strip()

    year_cols = [c for c in df.columns if c != "region"]
    long_df = df.melt(id_vars=["region"], value_vars=year_cols, var_name="year", value_name="salary")

    long_df["salary"] = (
        long_df["salary"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    long_df["salary"] = pd.to_numeric(long_df["salary"], errors="coerce")
    long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce")

    long_df = long_df.dropna(subset=["year", "salary"])
    long_df["year"] = long_df["year"].astype(int)
    return long_df


def main() -> int:
    if not RAW_FILE.exists():
        print("ERROR: Raw file not found. Run:")
        print("  python src/data_load.py")
        return 2

    df = read_csv_auto_sep(RAW_FILE)
    long_df = to_long(df)

    # 1) Average salary by year (mean across regions)
    avg_by_year = long_df.groupby("year")["salary"].mean().sort_index()
    plt.figure()
    avg_by_year.plot()
    plt.title("Average salary by year (mean across regions)")
    plt.xlabel("Year")
    plt.ylabel("Salary (UAH)")
    plt.tight_layout()
    out1 = FIG_DIR / "avg_salary_by_year.png"
    plt.savefig(out1, dpi=150)
    plt.close()
    print("Saved:", out1)

    # 2) Top-10 regions by salary in last year
    last_year = int(long_df["year"].max())
    top10 = (
        long_df[long_df["year"] == last_year]
        .groupby("region")["salary"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure()
    top10.sort_values().plot(kind="barh")
    plt.title(f"Top-10 regions by salary ({last_year})")
    plt.xlabel("Salary (UAH)")
    plt.ylabel("Region")
    plt.tight_layout()
    out2 = FIG_DIR / "top10_regions_last_year.png"
    plt.savefig(out2, dpi=150)
    plt.close()
    print("Saved:", out2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
