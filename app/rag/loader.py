from pathlib import Path
import pymupdf


def load_pdf(file_path: str) -> list[dict]:
    """Extract text from a PDF page by page."""

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()

        if text:
            pages.append({
                "text": text,
                "source": Path(file_path).name,
                "page": page_number
            })

    document.close()

    return pages


def load_documents(directory: str) -> list[dict]:
    """Load all PDF files from a directory."""

    documents = []

    for file_path in Path(directory).glob("*.pdf"):
        documents.extend(load_pdf(str(file_path)))

    return documents