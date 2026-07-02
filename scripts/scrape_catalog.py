"""
Module: Catalog Downloader
Purpose: Download the SHL Product Catalog HTML for inspection.

Author: Pruthviraj Khot
Project: SHL Conversational Assessment Recommender
"""

import requests
from pathlib import Path

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

OUTPUT_FILE = Path("data/catalog_page.html")


def download_catalog():
    """
    Downloads the SHL Product Catalog page
    and stores the HTML locally.
    """

    print("Downloading SHL Product Catalog...")

    response = requests.get(
        CATALOG_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/137 Safari/537.36"
            )
        },
        timeout=30,
    )

    response.raise_for_status()

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    OUTPUT_FILE.write_text(response.text, encoding="utf-8")

    print(f"Saved HTML to {OUTPUT_FILE}")


if __name__ == "__main__":
    download_catalog()