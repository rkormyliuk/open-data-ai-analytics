# src/data_load.py
from __future__ import annotations

from pathlib import Path
import sys
import urllib.request

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ВАЖЛИВО: встав сюди прямі download-лінки з data.gov.ua для queue.csv та busQueue.csv
# Їх можна взяти на сторінці датасету у розділі "Дані та ресурси" → конкретний ресурс → "Завантажити".
URLS = {
    "queue.csv": "</Users/romankormiluk/Desktop/DevOps/open-data-ai-analytics/queues.csv>",
    "busQueue.csv": "</Users/romankormiluk/Desktop/DevOps/open-data-ai-analytics/busqueue.csv>",
}

def download(url: str, out_path: Path) -> None:
    print(f"Downloading: {url} -> {out_path}")
    urllib.request.urlretrieve(url, out_path)

def main() -> int:
    missing = [k for k, v in URLS.items() if "<PASTE_" in v]
    if missing:
        print("ERROR: Please paste real download URLs for:", ", ".join(missing))
        return 2

    for filename, url in URLS.items():
        out_path = DATA_DIR / filename
        download(url, out_path)

    print("Done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())