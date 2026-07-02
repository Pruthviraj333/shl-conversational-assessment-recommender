"""
Build embeddings and FAISS index from the SHL catalog.
"""
from tqdm import tqdm
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INPUT_FILE = Path("data/processed/catalog.json")

INDEX_FILE = Path("data/index/faiss.index")
META_FILE = Path("data/index/metadata.json")

INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

print("Loading catalog...")

with open(INPUT_FILE, "r", encoding="utf8") as f:
    catalog = json.load(f)

print(f"{len(catalog)} assessments loaded.")


def build_embedding_text(item):

    important_paragraphs = item.get("paragraphs", [])[:4]

    text = f"""
Assessment:
{item.get("name","")}

Category:
{item.get("keys","")}

Test Type:
{item.get("test_type","")}

Duration:
{item.get("duration","")}

Languages:
{item.get("languages","")}

Description:
{item.get("meta_description","")}

Content:
{' '.join(important_paragraphs)}
"""

    return text.strip()


print("Preparing embedding texts...")

texts = []

for item in tqdm(catalog, desc="Preparing texts"):

    embedding_text = build_embedding_text(item)

    item["embedding_text"] = embedding_text

    texts.append(embedding_text)

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    convert_to_numpy=True,
    show_progress_bar=True,
)

embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

faiss.normalize_L2(embeddings)

index.add(embeddings)

faiss.write_index(
    index,
    str(INDEX_FILE),
)

with open(
    META_FILE,
    "w",
    encoding="utf8",
) as f:

    json.dump(
        catalog,
        f,
        indent=2,
        ensure_ascii=False,
    )

print()
print("=" * 60)
print("Embeddings Created Successfully")
print(f"Dimension : {dimension}")
print(f"Documents : {len(catalog)}")
print(f"Index      : {INDEX_FILE}")
print(f"Metadata   : {META_FILE}")
print("=" * 60)