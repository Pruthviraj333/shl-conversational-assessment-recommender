"""
Extract all SHL assessment recommendations from
the sample conversation markdown files.

Output:
data/processed/trace_catalog.json
"""

import json
import re
from pathlib import Path

INPUT_DIR = Path("sample_conversations")
OUTPUT_FILE = Path("data/processed/trace_catalog.json")

# Matches markdown table rows like:
# | 1 | OPQ32r | P | ... | ... | ... | https://... |
ROW_PATTERN = re.compile(
    r'^\|\s*\d+\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*<?(https?://[^>|]+)>?\s*\|$'
)

catalog = {}


for md_file in sorted(INPUT_DIR.glob("*.md")):

    print(f"Reading {md_file.name}")

    text = md_file.read_text(
        encoding="utf8"
    )

    for line in text.splitlines():

        match = ROW_PATTERN.match(line)

        if not match:
            continue

        name = match.group(1).strip()

        test_type = match.group(2).strip()

        keys = match.group(3).strip()

        duration = match.group(4).strip()

        languages = match.group(5).strip()

        url = match.group(6).strip()

        catalog[name] = {
            "name": name,
            "url": url,
            "test_type": test_type,
            "keys": keys,
            "duration": duration,
            "languages": languages,
        }


        OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf8"
) as f:

    json.dump(
        list(catalog.values()),
        f,
        indent=2,
        ensure_ascii=False,
    )

print("\n")
print("=" * 60)
print("Unique assessments:", len(catalog))
print("Saved:", OUTPUT_FILE)
print("=" * 60)