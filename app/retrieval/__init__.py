def __init__(self):

    index_path = Path("data/index/faiss.index")
    metadata_path = Path("data/index/metadata.json")

    self.index = faiss.read_index(str(index_path))

    with open(metadata_path, "r", encoding="utf-8") as f:
        self.catalog = json.load(f)

    # Lazy loading
    self.model = None

    print(f"Retriever loaded ({len(self.catalog)} assessments)")