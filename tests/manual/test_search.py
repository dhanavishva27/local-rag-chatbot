from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


embedding_model = EmbeddingModel()
vector_store = VectorStore()


question = "What is this document about?"


query_embedding = embedding_model.encode(
    [question]
)[0]


results = vector_store.search(
    query_embedding,
    n_results=5
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i, document in enumerate(documents):

    print("\n==============================")

    print("Result:", i + 1)

    print("Source:", metadatas[i]["source"])

    print("Page:", metadatas[i]["page"])

    print("Distance:", distances[i])

    print("\nText:")
    print(document[:500])