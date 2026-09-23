# Local RAG Document Q&A Chatbot

A fully local **Retrieval-Augmented Generation (RAG)** document question-answering chatbot built using **Ollama, Llama 3.2 3B, Sentence Transformers, ChromaDB, FastAPI, and HTML/CSS/JavaScript**.

The application allows users to ask questions about ingested PDF documents. Relevant document chunks are retrieved using semantic similarity, provided as context to a locally running LLM, and used to generate grounded answers with source document and page references.

---

## 1. Project Overview

Large Language Models can generate natural-language answers, but they do not automatically know the contents of private documents.

This project solves that problem using **Retrieval-Augmented Generation (RAG)**.

The system follows this workflow:

```text
PDF Documents
      ↓
Text Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
ChromaDB Vector Storage
      ↓
User Question
      ↓
Question Embedding
      ↓
Semantic Search
      ↓
Relevant Document Chunks
      ↓
Prompt + Retrieved Context
      ↓
Llama 3.2 3B through Ollama
      ↓
Grounded Answer
      ↓
Source Citations
```

The LLM is run locally, so the application does not require an external LLM API.

---

## 2. Key Features

* Fully local LLM inference using Ollama
* Llama 3.2 3B language model
* PDF document ingestion
* Text extraction using PyMuPDF
* Overlapping text chunking
* Semantic embeddings using `all-MiniLM-L6-v2`
* Local vector database using ChromaDB
* Semantic similarity search
* Retrieval relevance threshold
* Context-grounded answer generation
* Source document and page references
* FastAPI REST backend
* Simple responsive web chat interface
* Health-check API
* Environment-based configuration
* Application logging
* Automated tests
* Manual testing scripts

---

## 3. Technology Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python                 |
| LLM                  | Llama 3.2 3B           |
| Local LLM Runtime    | Ollama                 |
| RAG                  | Custom Python pipeline |
| PDF Processing       | PyMuPDF                |
| Embeddings           | Sentence Transformers  |
| Embedding Model      | all-MiniLM-L6-v2       |
| Vector Database      | ChromaDB               |
| Backend              | FastAPI                |
| Frontend             | HTML, CSS, JavaScript  |
| HTTP Client          | Requests               |
| Testing              | Pytest                 |
| Configuration        | python-dotenv          |
| Version Control      | Git / GitHub           |

---

## 4. Architecture

```text
                         User
                          │
                          │ Question
                          ▼
                 ┌──────────────────┐
                 │   Web Frontend   │
                 │ HTML/CSS/JS      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     FastAPI      │
                 │    /chat API     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   RAG Pipeline   │
                 └────────┬─────────┘
                          │
                    Question
                    Embedding
                          │
                          ▼
                 ┌──────────────────┐
                 │    ChromaDB      │
                 │ Vector Search    │
                 └────────┬─────────┘
                          │
                    Relevant
                     Chunks
                          │
                          ▼
                 ┌──────────────────┐
                 │      Ollama      │
                 │   Llama 3.2 3B  │
                 └────────┬─────────┘
                          │
                       Answer
                          │
                          ▼
                 ┌──────────────────┐
                 │ FastAPI Response │
                 │ + Sources        │
                 └────────┬─────────┘
                          │
                          ▼
                         User
```

---

## 5. RAG Workflow

### Step 1 — Document Loading

PDF files are placed inside:

```text
data/documents/
```

PyMuPDF extracts text from each page.

Each page is stored with metadata:

```python
{
    "text": "...",
    "source": "NeerRaksha.pdf",
    "page": 1
}
```

---

### Step 2 — Text Chunking

Large documents are divided into smaller pieces called **chunks**.

The project uses:

```text
Chunk size: 1000 characters
Overlap: 200 characters
```

The overlap helps preserve context between neighboring chunks.

Each chunk receives a unique ID such as:

```text
NeerRaksha_page_1_chunk_0
```

---

### Step 3 — Embedding Generation

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The model generates a **384-dimensional embedding**.

Conceptually:

```text
Text
 ↓
Sentence Transformer
 ↓
[0.12, -0.04, 0.72, ...]
```

These vectors represent the semantic meaning of the text.

---

### Step 4 — Vector Storage

The embeddings are stored in ChromaDB along with:

* Original chunk text
* Source document
* Page number
* Unique chunk ID

This allows the system to search documents based on semantic meaning rather than exact keyword matching.

---

### Step 5 — User Question

The user asks a question through the web interface.

Example:

```text
What problem does NeerRaksha solve?
```

The frontend sends the question to:

```text
POST /chat
```

---

### Step 6 — Question Embedding

The question is converted into an embedding using the same embedding model:

```text
Question
   ↓
all-MiniLM-L6-v2
   ↓
384-dimensional vector
```

---

### Step 7 — Semantic Retrieval

The question vector is compared with the vectors stored in ChromaDB.

The closest chunks are retrieved.

The default number of retrieved chunks is:

```text
RETRIEVAL_TOP_K=5
```

---

### Step 8 — Relevance Filtering

Retrieved chunks are filtered using:

```text
RETRIEVAL_MAX_DISTANCE=1.90
```

If no retrieved chunk is sufficiently relevant, the system returns:

```text
I couldn't find this information in the provided documents.
```

This prevents the LLM from generating answers from unrelated document content.

---

### Step 9 — Prompt Construction

Relevant chunks are inserted into a prompt.

The prompt instructs the LLM to:

* Use only the supplied context
* Avoid unsupported information
* Avoid hallucinating
* Include citations
* Return a clear answer

Example:

```text
[SOURCE 1]

Document: NeerRaksha.pdf
Page: 1

Content:
...
```

---

### Step 10 — Local LLM Generation

The prompt is sent to:

```text
Ollama
    ↓
Llama 3.2 3B
```

Ollama runs the model locally and returns the generated response.

---

### Step 11 — Source Citations

The response contains source information such as:

```text
NeerRaksha.pdf — Page 1
```

The LLM is also instructed to cite factual statements using:

```text
[SOURCE 1]
```

This helps users trace the answer back to the retrieved document content.

---

## 6. Project Structure

```text
local-rag-chatbot/
│
├── app/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
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
│   ├── llm/
│   │   ├── __init__.py
│   │   └── ollama_client.py
│   │
│   ├── logger.py
│   └── main.py
│
├── data/
│   ├── documents/
│   │   ├── NeerRaksha.pdf
│   │   └── sample.pdf.pdf
│   │
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
│   ├── test_loader.py
│   │
│   └── manual/
│       ├── manual_loader_test.py
│       ├── rag_manual.py
│       ├── retrieval_manual.py
│       ├── test_chunking.py
│       ├── test_embeddings.py
│       ├── test_llm.py
│       ├── test_ollama.py
│       └── test_search.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 7. Main Components

### `loader.py`

Responsible for extracting text from PDF files using PyMuPDF.

```text
PDF → Page text + metadata
```

---

### `splitter.py`

Splits extracted text into overlapping chunks.

```text
Large text → Smaller chunks
```

---

### `chunker.py`

Creates structured chunks and unique IDs while preserving:

* Source
* Page number
* Text

---

### `embeddings.py`

Loads the Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

and converts text into embeddings.

---

### `vector_store.py`

Handles ChromaDB operations:

```text
Store embeddings
Retrieve similar chunks
```

---

### `pipeline.py`

Combines the complete RAG process:

```text
Question
 ↓
Embedding
 ↓
Retrieval
 ↓
Relevance filtering
 ↓
Context construction
 ↓
LLM generation
 ↓
Answer + sources
```

---

### `ollama_client.py`

Communicates with the locally running Ollama API.

Default endpoint:

```text
http://localhost:11434/api/generate
```

---

### `routes.py`

Defines FastAPI endpoints:

```text
GET  /health
POST /chat
```

---

### `main.py`

Creates the FastAPI application and serves the frontend.

---

### `scripts/ingest.py`

Runs document ingestion:

```text
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

---

## 8. Prerequisites

Install the following:

### Python

Python 3.10+ recommended.

Verify:

```powershell
python --version
```

### Ollama

Install Ollama and verify:

```powershell
ollama --version
```

Download the required model:

```powershell
ollama pull llama3.2:3b
```

Verify available models:

```powershell
ollama list
```

You should see:

```text
llama3.2:3b
```

---

## 9. Installation

Clone the repository:

```powershell
git clone https://github.com/dhanavishva27/local-rag-chatbot.git
```

Enter the project:

```powershell
cd local-rag-chatbot
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 10. Environment Configuration

Create a `.env` file in the project root:

```env
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:3b
RETRIEVAL_TOP_K=5
RETRIEVAL_MAX_DISTANCE=1.90
```

`.env` is excluded from Git using `.gitignore`.

A sample configuration is provided in:

```text
.env.example
```

---

## 11. Add Documents

Place PDF files inside:

```text
data/documents/
```

Example:

```text
data/documents/
├── NeerRaksha.pdf
└── another-document.pdf
```

The application currently processes PDF documents already placed in this directory.

---

## 12. Run Document Ingestion

Before asking questions, process the documents:

```powershell
python -m scripts.ingest
```

Expected workflow:

```text
Loading documents...
Loaded X pages.

Creating chunks...
Created X chunks.

Generating embeddings...
Embeddings generated.

Storing in ChromaDB...
Ingestion completed successfully.
```

This creates the local ChromaDB data under:

```text
data/chroma/
```

---

## 13. Start the Application

Make sure Ollama is running.

Then start FastAPI:

```powershell
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

Open this address in a browser.

---

## 14. API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

---

## 15. API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "message": "RAG API is running"
}
```

---

### Chat

```http
POST /chat
```

Request:

```json
{
  "question": "What problem does NeerRaksha solve?"
}
```

Response:

```json
{
  "answer": "NeerRaksha addresses ... [SOURCE 1]",
  "sources": [
    {
      "source": "NeerRaksha.pdf",
      "page": 1
    }
  ]
}
```

---

## 16. Example Questions

Questions that can be answered from the provided documents include:

```text
What problem does NeerRaksha solve?

What are the main features of the project?

What technologies are used?

What are the candidate's technical skills?
```

Questions unrelated to the ingested documents should result in:

```text
I couldn't find this information in the provided documents.
```

For example:

```text
What is the capital of France?
```

if that information is not present in the documents.

---

## 17. Testing

Run automated tests with:

```powershell
pytest
```

The automated tests cover important functionality such as:

* PDF loading
* Chunk creation
* API behavior

Manual experiments are available under:

```text
tests/manual/
```

These scripts were used during development to verify:

* PDF extraction
* Chunking
* Embedding generation
* Ollama communication
* Vector retrieval
* RAG responses

---

## 18. Logging

The application includes logging for important operations.

Logs are written to:

```text
logs/app.log
```

The log system records events such as:

```text
Document retrieval
Retrieved chunk distances
Number of relevant chunks
Ollama requests
Ollama responses
Generated answers
Errors
```

The `logs/` directory is excluded from Git.

---

## 19. Configuration Parameters

### `OLLAMA_URL`

Defines the local Ollama API endpoint.

Default:

```env
OLLAMA_URL=http://localhost:11434/api/generate
```

---

### `OLLAMA_MODEL`

Defines the LLM used by the application.

Default:

```env
OLLAMA_MODEL=llama3.2:3b
```

---

### `RETRIEVAL_TOP_K`

Defines how many chunks are initially retrieved.

Default:

```env
RETRIEVAL_TOP_K=5
```

---

### `RETRIEVAL_MAX_DISTANCE`

Defines the maximum accepted retrieval distance.

Default:

```env
RETRIEVAL_MAX_DISTANCE=1.90
```

This helps prevent unrelated chunks from being passed to the LLM.

---

## 20. Important Design Decisions

### Local LLM

The project uses Ollama and Llama 3.2 3B instead of an external cloud LLM API.

Benefits include:

* Local execution
* No external LLM API key
* Document data remains within the local application environment
* Suitable for demonstrating local RAG architecture

---

### Semantic Search

The system uses embeddings instead of simple keyword matching.

This allows semantically related text to be retrieved even when the exact words in the question are different from the document.

---

### Retrieval Threshold

Vector databases can return the closest available chunks even when none are actually useful.

The relevance threshold provides an additional filtering layer before context is sent to the LLM.

---

### Source Tracking

Each chunk stores its:

```text
Source document
Page number
```

This allows the application to provide document references with answers.

---

## 21. Assumptions

* Input documents are PDF files.
* PDFs contain extractable text.
* Documents are manually placed in `data/documents/`.
* Document ingestion is performed before querying new documents.
* Ollama is running locally.
* The required Llama model is already available through Ollama.
* The embedding model is downloaded automatically by Sentence Transformers when required.
* ChromaDB is used as the local vector database.
* Answers should be based only on retrieved document context.

---

## 22. Difficulties Encountered

### 1. Multi-document chunk ID collisions

Initially, chunks could generate identical IDs when different documents contained the same page and chunk numbers.

This was solved by including the document name in the chunk ID:

```text
NeerRaksha_page_1_chunk_0
sample_page_1_chunk_0
```

---

### 2. Irrelevant retrieval

The vector database can always return some chunks, even if the question is unrelated to the documents.

A retrieval distance threshold was introduced:

```text
RETRIEVAL_MAX_DISTANCE=1.90
```

If no chunk passes the threshold, the system returns a document-not-found response.

---

### 3. Source citation handling

The system needs to preserve source information throughout the RAG pipeline.

Source and page metadata are stored with each chunk and returned in the API response.

---

### 4. Local LLM communication

The application communicates with Ollama through its local HTTP API.

The Ollama client includes request handling, timeout handling, and error logging.

---

### 5. Testing during development

Individual components were tested separately before integrating the complete pipeline.

Manual tests were used during development, while automated tests were added for important application functionality.

---

## 23. Other Observations

* RAG does not require retraining the LLM on every new document.
* The LLM and embedding model are separate components.
* The embedding model is responsible for semantic representation and retrieval.
* The LLM is responsible for generating the final natural-language answer.
* ChromaDB stores vectors and associated document metadata.
* Ollama provides a local interface for running the Llama model.
* The application can support additional PDF documents by placing them in the document directory and rerunning ingestion.
* The quality of retrieval depends on chunk size, overlap, embedding model, and retrieval threshold.
* The quality of generated answers also depends on the quality and relevance of retrieved context.

---

## 24. Future Enhancements

Possible future improvements include:

* Support for additional document formats
* Improved chunking strategies
* Hybrid keyword + semantic retrieval
* Reranking retrieved chunks
* Conversation memory
* Streaming LLM responses
* Better citation highlighting
* Document management interface
* Authentication and user accounts
* Automated document ingestion
* Evaluation datasets and retrieval metrics
* Docker-based deployment
* Automated CI/CD
* More extensive automated test coverage

---

## 25. Development Time

Approximate development time:

```text
Environment setup                 : Completed
PDF ingestion                     : Completed
Chunking                          : Completed
Embedding generation              : Completed
ChromaDB integration              : Completed
RAG pipeline                      : Completed
Ollama integration                : Completed
FastAPI backend                   : Completed
Frontend                          : Completed
Source citation handling          : Completed
Testing                           : Completed
Logging                           : Completed
Documentation                     : Completed
GitHub setup                      : Completed
```

---

## 26. Running the Complete Project

The complete workflow is:

### 1. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Make sure Ollama is available

```powershell
ollama list
```

### 3. Add PDFs

```text
data/documents/
```

### 4. Run ingestion

```powershell
python -m scripts.ingest
```

### 5. Start FastAPI

```powershell
uvicorn app.main:app --reload
```

### 6. Open the application

```text
http://127.0.0.1:8000/
```

### 7. Ask questions

Example:

```text
What problem does NeerRaksha solve?
```

---

## 27. Project Repository

GitHub:

https://github.com/dhanavishva27/local-rag-chatbot

---

## 28. License

This project was created as an academic/technical project for demonstrating a local Retrieval-Augmented Generation document question-answering system.
