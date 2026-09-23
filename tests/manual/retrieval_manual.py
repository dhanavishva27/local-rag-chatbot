import os

from dotenv import load_dotenv

from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


load_dotenv()


MAX_DISTANCE = float(
    os.getenv(
        "RETRIEVAL_MAX_DISTANCE",
        "1.90"
    )
)


embedding_model = EmbeddingModel()
vector_store = VectorStore()


question = input("Enter your question: ")


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


print("\n================================")
print("RETRIEVAL RESULTS")
print("================================")


for index, (
    document,
    metadata,
    distance
) in enumerate(
    zip(
        documents,
        metadatas,
        distances
    ),
    start=1
):

    print(f"\nResult {index}")

    print(
        f"Source: {metadata['source']}"
    )

    print(
        f"Page: {metadata['page']}"
    )

    print(
        f"Distance: {distance:.4f}"
    )

    print(
        f"Relevant: {distance <= MAX_DISTANCE}"
    )

    print("\nText:")
    print(document[:300])