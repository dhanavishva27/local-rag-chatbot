import chromadb


class VectorStore:

    def __init__(self, path: str = "data/chroma"):

        self.client = chromadb.PersistentClient(
            path=path
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(
        self,
        chunks: list[dict],
        embeddings: list[list[float]]
    ):
        """Store chunks and their embeddings in ChromaDB."""

        self.collection.upsert(
            ids=[chunk["id"] for chunk in chunks],

            documents=[
                chunk["text"]
                for chunk in chunks
            ],

            embeddings=embeddings,

            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
                for chunk in chunks
            ]
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5
    ):
        """Search for the most similar document chunks."""

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results