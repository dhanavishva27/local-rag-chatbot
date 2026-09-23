# Local RAG Document Q&A Chatbot

A fully local Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about multiple PDF documents.

The system uses Ollama with Llama 3.2 for local answer generation, Sentence Transformers for semantic embeddings, and ChromaDB for vector storage and retrieval.

---

## 1. Project Overview

This project implements a local document question-answering system using Retrieval-Augmented Generation.

Users can ask questions about the uploaded/ingested PDF documents. The system retrieves relevant document chunks and provides them as context to a locally running LLM.

The chatbot answers using only the retrieved document information and provides source document and page references.

No external LLM API is required.

---

## 2. Key Features

- Fully local LLM using Ollama
- Llama 3.2:3b for answer generation
- PDF text extraction using PyMuPDF
- Text chunking with overlapping chunks
- Semantic embeddings using `all-MiniLM-L6-v2`
- Local vector database using ChromaDB
- Multi-document retrieval
- Relevance filtering
- Grounded responses using retrieved context
- Source document and page citations
- FastAPI backend
- Web-based chatbot interface
- Configurable environment variables
- Application logging
- Automated tests using pytest

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM | Llama 3.2:3b |
| LLM Runtime | Ollama |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest |
| Configuration | python-dotenv |

---

## 4. System Architecture

```text
                    PDF Documents
                         |
                         v
                  PDF Text Extraction
                      PyMuPDF
                         |
                         v
                    Text Chunking
                         |
                         v
                  Embedding Model
              all-MiniLM-L6-v2
                         |
                         v
                     ChromaDB
                  Vector Database
                         |
                         |
User Question ----------+
       |
       v
Query Embedding
       |
       v
Semantic Retrieval
       |
       v
Relevant Document Chunks
       |
       v
Context + Question
       |
       v
Llama 3.2:3b
       |
       v
Grounded Answer
       |
       v
Source Citations

5. RAG Workflow
Step 1 — Document Loading

PDF files are read using PyMuPDF.

Each page is extracted separately while preserving:

Document name
Page number
Text
Step 2 — Chunking

Large text sections are divided into smaller chunks.

Current configuration:

Chunk size: 1000 characters
Chunk overlap: 200 characters

The overlap helps preserve context between neighboring chunks.

Step 3 — Embeddings

The all-MiniLM-L6-v2 Sentence Transformer converts each chunk into a numerical embedding vector.

These vectors represent the semantic meaning of the text.

Step 4 — Vector Storage

The embeddings and document metadata are stored locally in ChromaDB.

Each chunk stores:

Chunk ID
Text
Source document
Page number
Embedding
Step 5 — Question Retrieval

When a user asks a question:

The question is converted into an embedding.
ChromaDB searches for semantically similar chunks.
The top matching chunks are retrieved.
A relevance distance threshold is applied.
Step 6 — Context Augmentation

The retrieved chunks are combined into a context passed to the LLM.

Step 7 — Local Generation

Llama 3.2:3b running through Ollama generates the final answer.

The model is instructed to:

Use only retrieved context
Avoid unsupported information
Provide source references
State when information cannot be found
Step 8 — Source References

The API returns the source document and page number for the retrieved context.

Example:

Sources

sample.pdf.pdf — Page 1
NeerRaksha.pdf — Page 8
6. Project Structure
local-rag-chatbot/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── ollama_client.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── pipeline.py
│   │
│   ├── logger.py
│   └── main.py
│
├── data/
│   ├── documents/
│   └── chroma/
│
├── scripts/
│   ├── __init__.py
│   └── ingest.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_chunker.py
│   └── test_loader.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
7. Prerequisites

Install the following:

Python 3.12+
Ollama
Git

The application is designed to run locally.

8. Ollama Setup

Install Ollama and verify that it is available:

ollama --version

Download the required model:

ollama pull llama3.2:3b

Test the model:

ollama run llama3.2:3b

The application communicates with Ollama through its local API:

http://localhost:11434/api/generate
9. Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd local-rag-chatbot

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
10. Environment Configuration

Create a .env file in the project root:

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:3b
RETRIEVAL_TOP_K=5
RETRIEVAL_MAX_DISTANCE=1.90

Do not commit the .env file to GitHub.

11. Add Documents

Place PDF files inside:

data/documents/

Example:

data/documents/
├── sample.pdf.pdf
└── NeerRaksha.pdf
12. Document Ingestion

Run:

python -m scripts.ingest

The ingestion pipeline:

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
ChromaDB

The vector database is generated locally.

13. Run the Application

Start the FastAPI server:

python -m uvicorn app.main:app --reload

Open the chatbot:

http://127.0.0.1:8000/

API documentation:

http://127.0.0.1:8000/docs
14. API
Health Check
GET /health

Example response:

{
    "status": "ok",
    "message": "RAG API is running"
}
Chat
POST /chat

Request:

{
    "question": "What problem does NeerRaksha solve?"
}

Response:

{
    "answer": "Generated answer...",
    "sources": [
        {
            "source": "NeerRaksha.pdf",
            "page": 8
        }
    ]
}
15. Example Questions
Resume
What are his skills?
What is the name of the college?
NeerRaksha
What problem does NeerRaksha solve?
How does the system handle complaints?
What technologies are used in the system?
Out-of-context question
What is the capital of France?

Expected behavior:

I couldn't find this information in the provided documents.
16. Testing

Run the automated test suite:

pytest

The project includes tests for:

API health endpoint
Document chunking
PDF loading
17. Logging

Application logs are written to:

logs/app.log

The application logs information such as:

User questions
Retrieval operations
Retrieved distances
Number of relevant chunks
Ollama requests
Generation success/failure

Logs are excluded from Git using .gitignore.

18. Assumptions
Input documents are PDF files containing extractable text.
Ollama is installed and running locally.
The required Llama model is available locally.
The embedding model can be downloaded during initial setup.
The chatbot should answer only using information retrieved from the provided documents.
Scanned/image-only PDFs may require OCR and are not currently handled.
19. Challenges Encountered
Python Environment Configuration

The project required a properly configured Python virtual environment and package installation.

PDF Text Extraction

PDF content structure varies between documents, so text extraction quality can differ.

Retrieval Relevance

Initial distance filtering was too strict and rejected useful chunks.

The retrieval threshold was tuned using actual ChromaDB retrieval distances.

Multi-document Storage

Chunk IDs were redesigned to include document and page information so that chunks from different PDFs do not overwrite one another.

Local LLM Integration

Ollama was integrated through its local HTTP API so that generation remains local.

20. Development Time

Development time should be recorded based on the actual time spent implementing and testing the project.

Recommended format:

Task 2 — Local RAG Document Q&A Chatbot

Development and testing time:
[ADD ACTUAL TIME]
21. Other Observations
The complete LLM generation pipeline runs locally through Ollama.
ChromaDB stores embeddings locally.
No external LLM API is required.
Source document and page metadata are preserved throughout the retrieval pipeline.
The system supports multiple PDF documents.
The vector database can be regenerated using the ingestion script.
22. Future Improvements

Possible future enhancements include:

Web-based PDF upload
Improved document-aware chunking
OCR support for scanned PDFs
Streaming LLM responses
Conversation history
Advanced citation highlighting
Docker deployment
Authentication and access control
23. License

This project was developed as an academic/project assignment.


### One correction before you paste it

Don't actually claim **"uploaded documents"** in the README because we haven't implemented web upload. The README above says "uploaded/ingested" once; change that sentence to:

```markdown
Users can ask questions about the ingested PDF documents.