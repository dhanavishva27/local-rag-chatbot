from app.rag.embeddings import EmbeddingModel


model = EmbeddingModel()

texts = [
    "What is artificial intelligence?",
    "Machine learning is a branch of AI.",
    "I like eating pizza."
]

embeddings = model.encode(texts)

print("Number of texts:", len(embeddings))
print("Vector size:", len(embeddings[0]))

print("\nFirst few values:")
print(embeddings[0][:10])