from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/salary_by_region.csv")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OUT_REPORT = REPORTS_DIR / "data_quality_report.md"


def read_csv_robust(path: Path) -> tuple[pd.DataFrame, str, str, int]:
    """
    Returns: (df, encoding_used, sep_used, bad_lines_count)
    Detects separator from the first line and parses robustly.
    """
    encodings = ["utf-8", "cp1251"]
    last_err: Exception | None = None

    # Read first line to guess separator
    raw_first_line = path.read_bytes().splitlines()[:1]
    first_line_bytes = raw_first_line[0] if raw_first_line else b""

    for enc in encodings:
        try:
            first_line = first_line_bytes.decode(enc, errors="replace")
        except Exception as e:
            last_err = e
            continue

        # crude but effective guess: which separator appears more?
        comma_count = first_line.count(",")
        semicolon_count = first_line.count(";")
        sep = "," if comma_count >= semicolon_count else ";"

        bad_lines = {"count": 0}

        def bad_line_handler(bad_line: list[str]) -> None:
            bad_lines["count"] += 1
            return None  # skip line

        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                sep=sep,
                engine="python",
                dtype=str,
                on_bad_lines=bad_line_handler,
            )
            return df, enc, sep, bad_lines["count"]
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Failed to parse CSV. Last error: {last_err}")

def main() -> int:
    if not RAW_FILE.exists():
        print("ERROR: Raw file not found. Run data_load first:")
        print("  python src/data_load.py")
        return 2

    df, enc, sep, bad_lines_count = read_csv_robust(RAW_FILE)

    rows, cols = df.shape
    missing = df.isna().sum().sort_values(ascending=False)
    dup_rows = int(df.duplicated().sum())
    dtypes = df.dtypes.astype(str)

    # numeric-like columns sanity check
    numeric_cols = []
    negative_counts = {}
    for c in df.columns:
        s = pd.to_numeric(df[c].str.replace(",", ".", regex=False), errors="coerce")
        if s.notna().sum() >= max(3, int(0.1 * len(df))):
            numeric_cols.append(c)
            negative_counts[c] = int((s < 0).sum())

    with OUT_REPORT.open("w", encoding="utf-8") as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"**Dataset:** `{RAW_FILE}`\n\n")
        f.write(f"**Encoding used:** `{enc}`\n\n")
        f.write(f"**Separator used:** `{sep}`\n\n")
        f.write(f"**Skipped malformed lines:** **{bad_lines_count}**\n\n")
        f.write(f"**Rows loaded:** {rows}\n\n")
        f.write(f"**Columns:** {cols}\n\n")

        f.write("## Columns\n\n")
        for c in df.columns:
            f.write(f"- `{c}` ({dtypes[c]})\n")

        f.write("\n## Missing values (top)\n\n")
        top_missing = missing[missing > 0].head(15)
        if top_missing.empty:
            f.write("No missing values detected.\n")
        else:
            for c, v in top_missing.items():
                f.write(f"- `{c}`: {int(v)}\n")

        f.write("\n## Duplicate rows\n\n")
        f.write(f"Duplicate rows: **{dup_rows}**\n")

        f.write("\n## Numeric sanity checks\n\n")
        if not numeric_cols:
            f.write("No numeric-like columns detected.\n")
        else:
            f.write("Negative values count per numeric-like column:\n\n")
            for c in numeric_cols:
                f.write(f"- `{c}`: {negative_counts[c]}\n")

    print(f"Saved report: {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
