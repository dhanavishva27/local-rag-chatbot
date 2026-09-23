from app.rag.loader import load_documents


documents = load_documents("data/documents")

print(f"Pages loaded: {len(documents)}")

for document in documents[:3]:
    print("\n--------------------")
    print("Source:", document["source"])
    print("Page:", document["page"])
    print("Text:")
    print(document["text"][:500])