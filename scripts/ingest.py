from app.rag.loader import load_documents
from app.rag.chunker import create_chunks
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


DOCUMENT_DIRECTORY = "data/documents"


def main():

    print("Loading documents...")

    documents = load_documents(
        DOCUMENT_DIRECTORY
    )

    print(f"Loaded {len(documents)} pages.")

    if not documents:
        print("No PDF documents found.")
        return

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings...")

    embedding_model = EmbeddingModel()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(texts)

    print("Embeddings generated.")

    print("Storing in ChromaDB...")

    vector_store = VectorStore()

    vector_store.add_documents(
        chunks,
        embeddings
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()