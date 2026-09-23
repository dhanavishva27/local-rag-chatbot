from app.rag.loader import load_documents
from app.rag.chunker import create_chunks


documents = load_documents("data/documents")

chunks = create_chunks(documents)

print(f"Pages loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

for chunk in chunks[:5]:

    print("\n==============================")

    print("ID:", chunk["id"])
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])

    print("Text:")
    print(chunk["text"][:300])