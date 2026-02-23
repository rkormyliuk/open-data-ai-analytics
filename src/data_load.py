from __future__ import annotations

from pathlib import Path
import urllib.request

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATA_URL = "https://data.gov.ua/dataset/70b3dd1b-6c0b-44e1-a500-a6cd6533982f/resource/f0146832-4f94-43ce-a212-caa383803fd3/revision/130139/download"
OUT_FILE = RAW_DIR / "salary_by_region.csv"


def download(url: str, out_path: Path) -> None:
    print(f"Downloading from: {url}")
    urllib.request.urlretrieve(url, out_path)

    size = out_path.stat().st_size
    print(f"Saved to: {out_path} ({size} bytes)")


def main() -> int:
    if "PASTE_DIRECT_CSV_URL_HERE" in DATA_URL:
        print("ERROR: Insert direct CSV URL into DATA_URL")
        return 2

    download(DATA_URL, OUT_FILE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
