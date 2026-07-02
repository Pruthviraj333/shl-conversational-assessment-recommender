import json
import re
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:
    """
    Semantic Retriever using FAISS + Hybrid Re-ranking.
    """

    def __init__(self):
        index_path = Path("data/index/faiss.index")
        metadata_path = Path("data/index/metadata.json")

        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print(f"Retriever loaded ({len(self.catalog)} assessments)")

    def embed_query(self, query: str):
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
        ).astype(np.float32)

        faiss.normalize_L2(embedding)

        return embedding

    def rerank_score(self, item, query, semantic_score):
        """
        Hybrid scoring:
        - Semantic similarity
        - Exact name match
        - Keyword overlap
        - Category boost
        - Test type boost
        - Assessment vs Report heuristic
        """

        score = semantic_score

        query = query.lower()
        text = item.get("search_text", "").lower()
        name = item["name"].lower()

        # ---------------------------------------------------
        # Exact assessment name boost
        # ---------------------------------------------------

        if name in query:
            score += 0.50

        # ---------------------------------------------------
        # Keyword overlap
        # ---------------------------------------------------

        query_words = set(re.findall(r"\w+", query))
        text_words = set(re.findall(r"\w+", text))

        overlap = len(query_words & text_words)
        score += overlap * 0.03

        # ---------------------------------------------------
        # Category boost
        # ---------------------------------------------------

        if item.get("keys"):

            if item["keys"].lower() in query:
                score += 0.20

        # ---------------------------------------------------
        # Test type boost
        # ---------------------------------------------------

        if item.get("test_type"):

            if item["test_type"].lower() in query:
                score += 0.10

        # ---------------------------------------------------
        # Prefer assessments over reports
        # ---------------------------------------------------

        if "report" in name:
            score -= 0.20

        # ---------------------------------------------------
        # Personality heuristic
        # ---------------------------------------------------

        if "personality" in query:

            if (
                "occupational personality questionnaire" in name
                or "opq32r" in name
            ):
                score += 0.30

            if "report" in name:
                score -= 0.10

        # ---------------------------------------------------
        # Leadership heuristic
        # ---------------------------------------------------

        if "leadership" in query:

            if "leadership" in name:
                score += 0.20

        # ---------------------------------------------------
        # Coding heuristic
        # ---------------------------------------------------

        if "coding" in query or "developer" in query:

            if (
                "coding" in text
                or "java" in text
                or "programming" in text
            ):
                score += 0.20

        return score

    def search(self, query: str, top_k: int = 5):

        embedding = self.embed_query(query)

        # Retrieve more candidates than required
        scores, indices = self.index.search(
            embedding,
            15,
        )

        candidates = []

        for semantic_score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            item = self.catalog[idx].copy()

            item["semantic_score"] = float(semantic_score)

            item["score"] = self.rerank_score(
                item,
                query,
                float(semantic_score),
            )

            candidates.append(item)

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return candidates[:top_k]