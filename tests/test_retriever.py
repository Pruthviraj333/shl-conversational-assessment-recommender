from app.retrieval.retriever import Retriever

retriever = Retriever()

# ==========================================
# Change this query whenever you want to test
# ==========================================

query = """
Hiring graduate software engineers

Actually add personality assessment
"""

results = retriever.search(
    query=query,
    top_k=8,
)

print("\n" + "=" * 70)
print("QUERY")
print("=" * 70)
print(query)

print("\n" + "=" * 70)
print("TOP RESULTS")
print("=" * 70)

for i, item in enumerate(results, start=1):

    print(f"\n{i}. {item['name']}")
    print(f"Score      : {item['score']:.4f}")
    print(f"Type       : {item['test_type']}")
    print(f"Category   : {item['keys']}")
    print(f"URL        : {item['url']}")

    if item.get("meta_description"):
        print(f"Description: {item['meta_description']}")