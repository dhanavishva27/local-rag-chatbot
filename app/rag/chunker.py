from pathlib import Path

from app.rag.splitter import split_text


def create_chunks(documents: list[dict]) -> list[dict]:
    """
    Split loaded documents into chunks while preserving metadata.

    Each chunk gets a unique ID based on its source document.
    """

    chunks = []

    for document in documents:

        text_chunks = split_text(
            document["text"],
            chunk_size=1000,
            chunk_overlap=200
        )

        source_name = Path(
            document["source"]
        ).stem

        for chunk_index, chunk in enumerate(text_chunks):

            chunks.append({
                "id": (
                    f"{source_name}_"
                    f"page_{document['page']}_"
                    f"chunk_{chunk_index}"
                ),
                "text": chunk,
                "source": document["source"],
                "page": document["page"]
            })

    return chunks