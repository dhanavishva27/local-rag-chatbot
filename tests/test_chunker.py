from app.rag.chunker import create_chunks


def test_create_chunks():

    documents = [
        {
            "text": "This is a test document.",
            "source": "test.pdf",
            "page": 1
        }
    ]

    chunks = create_chunks(documents)

    assert len(chunks) > 0
    assert chunks[0]["source"] == "test.pdf"
    assert chunks[0]["page"] == 1

    assert chunks[0]["id"] == (
        "test_page_1_chunk_0"
    )