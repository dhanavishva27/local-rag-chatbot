from app.llm.ollama_client import generate_response


prompt = """
Explain Retrieval-Augmented Generation in simple terms.
"""


answer = generate_response(prompt)

print("\nLLM Response:")
print(answer)