"""
Enrich SHL assessment catalog with content scraped
from each assessment page.

Input:
    data/processed/trace_catalog.json

Output:
    data/processed/catalog.json
"""

import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

INPUT_FILE = Path("data/processed/trace_catalog.json")
OUTPUT_FILE = Path("data/processed/catalog.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean(text: str) -> str:
    """Remove extra whitespace."""
    return " ".join(text.split())


def get_page(url: str) -> BeautifulSoup:
    """Download page."""

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return BeautifulSoup(response.text, "lxml")


def extract_metadata(soup: BeautifulSoup):
    """
    Extract useful searchable text from product page.
    """

    # Title
    h1 = soup.find("h1")
    title = clean(h1.get_text()) if h1 else ""

    # Meta description
    meta = soup.find("meta", attrs={"name": "description"})
    meta_description = ""

    if meta:
        meta_description = clean(meta.get("content", ""))

    # Headings
    headings = []

    for tag in soup.find_all(["h2", "h3"]):
        text = clean(tag.get_text())

        if text:
            headings.append(text)

    # Paragraphs
    paragraphs = []

    for p in soup.find_all("p"):

        text = clean(p.get_text())

        if len(text) > 20:
            paragraphs.append(text)

    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "paragraphs": paragraphs,
    }


def build_search_text(item, metadata):
    """
    Create searchable text for embeddings.
    """

    chunks = [
        item.get("name", ""),
        item.get("keys", ""),
        item.get("test_type", ""),
        item.get("duration", ""),
        item.get("languages", ""),
        metadata["title"],
        metadata["meta_description"],
    ]

    chunks.extend(metadata["headings"])
    chunks.extend(metadata["paragraphs"])

    return "\n".join(
        chunk for chunk in chunks if chunk
    )


def main():

    with open(INPUT_FILE, "r", encoding="utf8") as f:
        catalog = json.load(f)

    enriched = []

    print(f"\nFound {len(catalog)} assessments\n")

    for item in tqdm(catalog):

        url = item["url"]

        try:

            soup = get_page(url)

            metadata = extract_metadata(soup)

            item["page_title"] = metadata["title"]
            item["meta_description"] = metadata["meta_description"]
            item["headings"] = metadata["headings"]
            item["paragraphs"] = metadata["paragraphs"]

            item["search_text"] = build_search_text(
                item,
                metadata,
            )

            enriched.append(item)

            time.sleep(0.5)

        except Exception as e:

            print(f"\nFailed: {url}")
            print(e)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf8",
    ) as f:

        json.dump(
            enriched,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 60)
    print(f"Saved {len(enriched)} enriched assessments")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()