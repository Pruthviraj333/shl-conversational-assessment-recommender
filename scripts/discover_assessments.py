"""
Recursive SHL Assessment URL Discovery
"""

from collections import deque
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.shl.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SEED_URLS = [
    "https://www.shl.com/products/assessments/",
]

visited = set()
assessment_urls = set()


def get_soup(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return BeautifulSoup(response.text, "lxml")


queue = deque(SEED_URLS)

while queue:

    url = queue.popleft()

    if url in visited:
        continue

    print("Visiting:", url)

    visited.add(url)

    try:

        soup = get_soup(url)

    except Exception as e:

        print(e)

        continue

    for a in soup.find_all("a", href=True):

        href = urljoin(BASE, a["href"])

        if "/products/assessments/" not in href:
            continue

        if href not in visited:

            queue.append(href)

        assessment_urls.add(href)


Path("data/raw").mkdir(parents=True, exist_ok=True)

outfile = Path("data/raw/assessment_urls.txt")

with open(outfile, "w", encoding="utf8") as f:

    for url in sorted(assessment_urls):

        f.write(url + "\n")

print("\n")
print("=" * 60)
print("Visited:", len(visited))
print("Assessment URLs:", len(assessment_urls))
print("=" * 60)