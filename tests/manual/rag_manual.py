from app.rag.pipeline import RAGPipeline


rag = RAGPipeline()


question = input("Ask a question about your document: ")


result = rag.ask(question)


print("\n================================")
print("ANSWER")
print("================================")

print(result["answer"])


print("\n================================")
print("SOURCES")
print("================================")

for source in result["sources"]:

    print(
        f"- {source['source']} "
        f"(Page {source['page']})"
    )