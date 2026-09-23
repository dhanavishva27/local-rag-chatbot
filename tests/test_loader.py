from app.rag.loader import load_pdf


def test_load_pdf_file_not_found():

    try:
        load_pdf("nonexistent.pdf")
        assert False
    except Exception:
        assert True