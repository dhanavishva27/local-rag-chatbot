import os

from dotenv import load_dotenv

from app.logger import logger
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.llm.ollama_client import generate_response


load_dotenv()


class RAGPipeline:
    """Complete Retrieval-Augmented Generation pipeline."""

    MAX_DISTANCE = float(
        os.getenv(
            "RETRIEVAL_MAX_DISTANCE",
            "1.90"
        )
    )

    TOP_K = int(
        os.getenv(
            "RETRIEVAL_TOP_K",
            "5"
        )
    )

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        question: str,
        n_results: int = 5
    ):
        """Retrieve relevant document chunks."""

        logger.info(
            "Retrieving documents for question: %s",
            question
        )

        query_embedding = self.embedding_model.encode(
            [question]
        )[0]

        results = self.vector_store.search(
            query_embedding,
            n_results=n_results
        )

        logger.info(
            "Retrieved %d chunks",
            len(results["documents"][0])
        )

        for distance in results["distances"][0]:

            logger.info(
                "Retrieved chunk distance: %.4f",
                distance
            )

        return results

    def generate_answer(
        self,
        question: str,
        results: dict
    ):
        """Generate a grounded answer with source citations."""

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        relevant_chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            if distance <= self.MAX_DISTANCE:

                relevant_chunks.append({
                    "text": document,
                    "source": metadata["source"],
                    "page": metadata["page"],
                    "distance": distance
                })

        logger.info(
            "Relevant chunks after filtering: %d",
            len(relevant_chunks)
        )

        # No relevant information found
        if not relevant_chunks:

            logger.info(
                "No relevant information found for question: %s",
                question
            )

            return {
                "answer": (
                    "I couldn't find this information "
                    "in the provided documents."
                ),
                "sources": []
            }

        # Build context with numbered source references
        context_parts = []

        for index, chunk in enumerate(
            relevant_chunks,
            start=1
        ):

            context_parts.append(
                f"[SOURCE {index}]\n"
                f"Document: {chunk['source']}\n"
                f"Page: {chunk['page']}\n"
                f"Content:\n{chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

IMPORTANT RULES:

1. Use only information contained in the context.
2. Do not use your general knowledge.
3. Do not invent or assume information.
4. Every factual statement must have a citation.
5. Use this citation format:

[SOURCE X]

where X is the source number provided in the context.
6. Put the citation immediately after the statement it supports.
7. If multiple sources support a statement, cite all of them.
8. If the answer cannot be found in the context, say exactly:

"I couldn't find this information in the provided documents."

9. Keep the answer clear and concise.
10. Do not mention the source numbering system in your answer.

Context:
====================

{context}

====================

Question:
{question}

Answer:
"""

        answer = generate_response(prompt).strip()

        logger.info(
            "Generated answer for question: %s",
            question
        )

        # Prepare structured source references
        sources = []

        seen = set()

        for chunk in relevant_chunks:

            key = (
                chunk["source"],
                chunk["page"]
            )

            if key not in seen:

                sources.append({
                    "source": chunk["source"],
                    "page": chunk["page"]
                })

                seen.add(key)

        return {
            "answer": answer,
            "sources": sources
        }

    def ask(
        self,
        question: str,
        n_results: int | None = None
    ):
        """Run the complete RAG pipeline."""

        if n_results is None:
            n_results = self.TOP_K

        results = self.retrieve(
            question,
            n_results
        )

        return self.generate_answer(
            question,
            results
        )