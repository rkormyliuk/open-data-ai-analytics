from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/salary_by_region.csv")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUT_REPORT = REPORTS_DIR / "data_research_report.md"


def read_csv_auto_sep(path: Path) -> pd.DataFrame:
    # detect separator from first line
    first_line = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    sep = "," if first_line.count(",") >= first_line.count(";") else ";"

    # robust read
    df = pd.read_csv(
        path,
        encoding="utf-8",
        sep=sep,
        engine="python",
        dtype=str,
        on_bad_lines="skip",
    )
    return df


def main() -> int:
    if not RAW_FILE.exists():
        print("ERROR: Raw file not found. Run data_load first:")
        print("  python src/data_load.py")
        return 2

    df = read_csv_auto_sep(RAW_FILE)

    # Clean columns
    df = df.rename(columns={df.columns[0]: "region"})
    df["region"] = df["region"].astype(str).str.strip()

    # Convert wide -> long: columns are years
    year_cols = [c for c in df.columns if c != "region"]
    long_df = df.melt(id_vars=["region"], value_vars=year_cols, var_name="year", value_name="salary")

    # Clean salary numeric
    long_df["salary"] = (
        long_df["salary"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    long_df["salary"] = pd.to_numeric(long_df["salary"], errors="coerce")
    long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce")

    # Drop bad rows
    long_df = long_df.dropna(subset=["year", "salary"])
    long_df["year"] = long_df["year"].astype(int)

    # Basic stats
    years = sorted(long_df["year"].unique().tolist())
    last_year = years[-1] if years else None

    avg_by_year = long_df.groupby("year")["salary"].mean().sort_index()
    top_regions_last_year = (
        long_df[long_df["year"] == last_year]
        .groupby("region")["salary"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        if last_year is not None
        else pd.Series(dtype=float)
    )

    with OUT_REPORT.open("w", encoding="utf-8") as f:
        f.write("# Data Research Report\n\n")
        f.write(f"**Dataset:** `{RAW_FILE}`\n\n")
        f.write(f"**Rows (long format):** {len(long_df)}\n\n")
        f.write(f"**Years available:** {years}\n\n")

        if last_year is not None:
            f.write(f"## Top-10 regions by salary (year {last_year})\n\n")
            for region, val in top_regions_last_year.items():
                f.write(f"- {region}: {val:.2f}\n")
            f.write("\n")

        f.write("## Average salary by year (mean across regions)\n\n")
        for y, val in avg_by_year.items():
            f.write(f"- {int(y)}: {val:.2f}\n")

    print(f"Saved report: {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
