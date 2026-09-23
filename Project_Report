# PROJECT REPORT

## Local LLM Document Q&A Chatbot using RAG

---

## 1. Project Overview

The **Local LLM Document Q&A Chatbot** is a Retrieval-Augmented Generation (RAG) application that allows users to ask questions about information contained in locally stored PDF documents.

The system processes PDF documents, extracts their text, divides the text into smaller chunks, converts the chunks into numerical embeddings, and stores them in a local **ChromaDB vector database**.

When a user asks a question, the system converts the question into an embedding and performs semantic similarity search against the stored document chunks. The most relevant chunks are then provided as context to a locally running **Llama 3.2 3B** model through **Ollama**.

The generated response is restricted to the retrieved document context and includes source references containing the document name and page number.

The entire RAG pipeline runs locally without requiring an external cloud-based LLM API.

---

# 2. Objectives

The main objectives of the project are:

* Build a completely local document question-answering system.
* Process PDF documents automatically.
* Extract text from PDF files using PyMuPDF.
* Split documents into manageable text chunks.
* Generate semantic embeddings using Sentence Transformers.
* Store and retrieve document chunks using ChromaDB.
* Use Ollama to run the Llama 3.2 3B local language model.
* Generate answers grounded in retrieved document content.
* Provide source references for generated answers.
* Prevent the model from answering questions that are unrelated to the indexed documents.
* Provide a simple web-based chatbot interface.
* Expose the RAG functionality through a FastAPI backend.
* Maintain logs and automated tests for reliability.

---

# 3. Technologies Used

| Technology            | Purpose                                |
| --------------------- | -------------------------------------- |
| Python                | Main programming language              |
| FastAPI               | Backend REST API                       |
| Ollama                | Local LLM runtime                      |
| Llama 3.2 3B          | Local language model                   |
| Sentence Transformers | Text embeddings                        |
| all-MiniLM-L6-v2      | Embedding model                        |
| ChromaDB              | Local vector database                  |
| PyMuPDF               | PDF text extraction                    |
| HTML/CSS/JavaScript   | Frontend chatbot                       |
| Requests              | Communication with Ollama              |
| Pytest                | Automated testing                      |
| python-dotenv         | Environment configuration              |
| Git/GitHub            | Version control and project submission |

---

# 4. System Architecture

The system follows a Retrieval-Augmented Generation architecture.

```text
                 PDF Documents
                       |
                       v
                  PyMuPDF
                       |
                       v
                 Text Extraction
                       |
                       v
                  Text Chunking
                       |
                       v
              Sentence Transformer
                       |
                       v
                 Embeddings
                       |
                       v
                   ChromaDB
                Vector Database
                       |
                       |
                 User Question
                       |
                       v
              Question Embedding
                       |
                       v
              Semantic Retrieval
                       |
                       v
               Relevant Chunks
                       |
                       v
             Prompt + Retrieved Context
                       |
                       v
                 Ollama Server
                       |
                       v
                Llama 3.2 3B
                       |
                       v
              Answer + Source References
                       |
                       v
                  Web Chat UI
```

---

# 5. Project Workflow

The system consists of two major stages:

1. Document ingestion
2. Question answering

---

## 5.1 Document Ingestion

The ingestion process prepares the documents for retrieval.

### Step 1: PDF Loading

PDF documents stored inside:

```text
data/documents/
```

are loaded using **PyMuPDF**.

The loader extracts text page by page and stores metadata such as:

* Document name
* Page number
* Extracted text

---

## 5.2 Text Chunking

Large documents cannot always be processed effectively as a single block.

Therefore, the extracted text is divided into smaller chunks.

The current configuration uses:

```text
Chunk size: 1000 characters
Chunk overlap: 200 characters
```

The overlap helps preserve contextual information between neighboring chunks.

Each chunk receives a unique identifier containing:

* Document name
* Page number
* Chunk number

Example:

```text
NeerRaksha_page_1_chunk_0
```

---

## 5.3 Embedding Generation

Each text chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The embedding model produces a **384-dimensional vector representation** for each chunk.

These vectors allow the system to compare the semantic meaning of the user question with the document content.

---

## 5.4 Vector Storage

The generated embeddings and their corresponding text are stored in:

```text
ChromaDB
```

ChromaDB is configured as a persistent local vector database.

The stored information includes:

* Chunk text
* Embedding
* Document name
* Page number
* Chunk ID

---

# 6. Question Answering Pipeline

When a user asks a question, the following process occurs.

### Step 1: User Question

Example:

```text
What problem does NeerRaksha solve?
```

### Step 2: Question Embedding

The question is converted into an embedding using the same:

```text
all-MiniLM-L6-v2
```

embedding model.

### Step 3: Semantic Search

The question embedding is compared with the embeddings stored in ChromaDB.

The system retrieves the most semantically relevant document chunks.

The default retrieval count is:

```text
Top K = 5
```

### Step 4: Relevance Filtering

Retrieved chunks are checked using a configurable distance threshold.

Current configuration:

```text
RETRIEVAL_MAX_DISTANCE = 1.90
```

Only sufficiently relevant chunks are passed to the generation stage.

### Step 5: Context Construction

The relevant chunks are combined into a context containing:

```text
Document name
Page number
Chunk content
```

### Step 6: Prompt Construction

The retrieved context and user question are provided to the Llama model through a structured prompt.

The prompt instructs the model to:

* Use only the supplied context.
* Avoid using general knowledge.
* Avoid inventing information.
* Cite factual statements.
* Return a predefined response when the information is unavailable.

### Step 7: Local LLM Generation

The prompt is sent to:

```text
Ollama
```

using its local API.

The selected model is:

```text
llama3.2:3b
```

### Step 8: Answer and Sources

The API returns:

```json
{
  "answer": "Generated answer...",
  "sources": [
    {
      "source": "NeerRaksha.pdf",
      "page": 1
    }
  ]
}
```

---

# 7. Source Citation

Source references are included to improve answer traceability.

For example:

```text
NeerRaksha addresses problems related to water-body protection. [SOURCE 1]
```

The API additionally returns the document and page:

```text
NeerRaksha.pdf
Page 1
```

This allows the user to identify where the information was retrieved from.

---

# 8. Handling Unrelated Questions

An important part of the project is preventing unsupported answers.

For example, if the indexed documents do not contain information about France and the user asks:

```text
What is the capital of France?
```

the system returns:

```text
I couldn't find this information in the provided documents.
```

No source is returned when no retrieved chunk passes the configured relevance threshold.

This demonstrates that the application is designed to provide **document-grounded answers rather than unrestricted general knowledge answers**.

---

# 9. Backend API

The backend is implemented using **FastAPI**.

## Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "ok",
  "message": "RAG API is running"
}
```

## Chat Endpoint

```text
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
  "answer": "Generated answer...",
  "sources": [
    {
      "source": "NeerRaksha.pdf",
      "page": 1
    }
  ]
}
```

FastAPI automatically provides interactive API documentation at:

```text
/docs
```

---

# 10. Frontend

A lightweight web interface was developed using:

* HTML
* CSS
* JavaScript

The interface provides:

* Question input
* Send button
* Chat-style conversation
* Generated answer display
* Source document display
* Page number display

The frontend communicates with the FastAPI backend.

The application can be accessed locally at:

```text
http://127.0.0.1:8000/
```

---

# 11. Project Structure

```text
local-rag-chatbot/
│
├── app/
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
│   └── chroma/
│
├── scripts/
│   └── ingest.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── test_api.py
│   ├── test_chunker.py
│   ├── test_loader.py
│   └── manual/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 12. Testing

Automated tests were created using **Pytest**.

The test suite covers important application components including:

### PDF Loader

Verifies that PDF documents can be loaded and page information is extracted correctly.

### Chunker

Verifies:

* Text splitting
* Chunk creation
* Chunk metadata
* Unique chunk identifiers

### API

Verifies API endpoints and request/response behavior.

Manual tests were also created for:

* Ollama connectivity
* Embedding generation
* Retrieval
* Search
* Complete RAG pipeline
* Chunking behavior

---

# 13. Difficulties Encountered

## 13.1 Python Environment Setup

The initial Python environment had PATH-related issues where the Python command was not immediately available.

A virtual environment was created and dependencies were installed inside it.

---

## 13.2 Ollama Configuration

The local LLM required Ollama to be installed and the required model to be downloaded.

The selected model was:

```text
llama3.2:3b
```

The application communicates with Ollama through:

```text
http://localhost:11434/api/generate
```

---

## 13.3 Retrieval Threshold

One of the main challenges was determining an appropriate similarity-distance threshold.

Some relevant questions initially produced distances higher than the first threshold used during testing.

The retrieval threshold was therefore made configurable through:

```text
RETRIEVAL_MAX_DISTANCE
```

The current value is:

```text
1.90
```

This allows the system to retrieve relevant information while filtering unrelated questions.

---

## 13.4 Multiple Document Chunk IDs

Initially, chunk identifiers could conflict when multiple documents contained the same page and chunk numbers.

This was solved by including the document name in the chunk ID.

Example:

```text
NeerRaksha_page_1_chunk_0
sample_page_1_chunk_0
```

---

## 13.5 Testing Unrelated Questions

Testing questions outside the document content showed that retrieval filtering needed to be handled carefully.

The final pipeline checks retrieved distances and returns:

```text
I couldn't find this information in the provided documents.
```

when no sufficiently relevant context is available.

---

## 13.6 Source Handling

The system was designed to return document and page metadata along with the answer.

This allows users to identify the source of retrieved information.

---

# 14. Assumptions

The following assumptions were made during development:

1. PDF documents are stored in the configured `data/documents/` directory.
2. The documents contain extractable text.
3. Ollama is installed and running locally.
4. The required Llama model is available locally.
5. The embedding model is available through Sentence Transformers.
6. ChromaDB is used as the local vector database.
7. Users ask questions related to the indexed documents.
8. The system does not require internet access for LLM inference.
9. Retrieval quality depends on document quality, chunking configuration, embedding quality, and the selected retrieval threshold.
10. Source citations identify the document and page from which the retrieved context originated.

---

# 15. Logging

Application logging was implemented using Python's `logging` module.

Logs contain information such as:

* Retrieval requests
* Number of retrieved chunks
* Retrieval distances
* Relevant chunk count
* Ollama requests
* Ollama responses
* Errors

Logs are stored in:

```text
logs/app.log
```

The `logs/` directory is excluded from Git using `.gitignore`.

---

# 16. Other Observations

The project demonstrates that a useful document Q&A application can be implemented entirely with local components.

The system separates the major RAG stages into independent modules:

```text
Loading
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Storage
   ↓
Retrieval
   ↓
Prompt Construction
   ↓
LLM Generation
```

This modular structure makes individual components easier to test, modify, and replace.

The project also demonstrates the difference between **retrieval** and **generation**:

* ChromaDB is responsible for finding relevant document content.
* The Llama model is responsible for generating a natural-language response from that retrieved context.

The local architecture also avoids sending document content to an external LLM API during normal inference.

---

# 17. Future Enhancements

Possible future improvements include:

### 17.1 Multiple File Formats

Support additional document formats such as:

* DOCX
* TXT
* Markdown
* HTML

### 17.2 Improved Chunking

Implement semantic or paragraph-based chunking instead of fixed character-based chunking.

### 17.3 Better Retrieval

Possible improvements include:

* Hybrid search
* Reranking
* Metadata filtering
* Improved similarity thresholds
* Query expansion

### 17.4 Conversation Memory

The chatbot could be extended to maintain conversation history and answer follow-up questions.

### 17.5 Streaming Responses

Ollama streaming could be implemented to display generated responses progressively.

### 17.6 Authentication

Authentication could be added if the application is deployed for multiple users.

### 17.7 Deployment

The system could be containerized using Docker and deployed on a suitable local or private server environment.

---

# 18. Development Time per Task

| Task                         | Approx. Time |
| ---------------------------- | -----------: |
| Planning and architecture    |       1.0 hr |
| Environment and dependencies |      0.75 hr |
| Ollama and model setup       |      0.75 hr |
| PDF loading                  |       1.0 hr |
| Text chunking                |       1.0 hr |
| Embedding implementation     |       1.0 hr |
| ChromaDB integration         |       1.5 hr |
| Document ingestion           |       1.0 hr |
| RAG retrieval pipeline       |       2.0 hr |
| Ollama integration           |       1.5 hr |
| Prompt and citation handling |       1.0 hr |
| Retrieval threshold tuning   |       1.0 hr |
| FastAPI backend              |       1.5 hr |
| Frontend implementation      |       1.5 hr |
| Testing and debugging        |       2.0 hr |
| Logging and configuration    |      0.75 hr |
| README and documentation     |       1.0 hr |
| Git/GitHub setup             |      0.75 hr |
| **Total**                    | **20.5 hrs** |

---

# 19. Submission Artifacts

The project submission contains the following major components:

* Source code
* RAG implementation
* PDF ingestion script
* Requirements file
* Environment configuration example
* Automated tests
* Manual testing scripts
* README documentation
* Sample PDF documents
* ChromaDB regeneration process
* Application logs
* Screenshots
* Demo video
* Project report
* Public GitHub repository

GitHub repository:

```text
https://github.com/dhanavishva27/local-rag-chatbot
```

---

# 20. Expected Output

For a question related to the indexed documents, the system should generate an answer based on retrieved document content and provide source information.

Example:

```text
Question:
What problem does NeerRaksha solve?

Answer:
[Generated answer based on the retrieved document context]

Source:
NeerRaksha.pdf
Page: 1
```

For information that is not available in the indexed documents:

```text
Question:
What is the capital of France?

Answer:
I couldn't find this information in the provided documents.

Sources:
None
```

---

# 21. Conclusion

The **Local LLM Document Q&A Chatbot** successfully implements a complete Retrieval-Augmented Generation pipeline using locally running components.

The system can ingest PDF documents, extract and chunk their content, generate semantic embeddings, store them in ChromaDB, retrieve relevant information for user questions, and use the locally running Llama 3.2 3B model through Ollama to generate grounded responses.

The application also provides source references, relevance filtering, a FastAPI backend, a web-based chatbot interface, logging, and automated tests.

The completed system demonstrates the practical implementation of core RAG concepts including:

```text
Document Ingestion
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
Semantic Retrieval
       ↓
Context Augmentation
       ↓
Local LLM Generation
       ↓
Source-Cited Answer
```

The project provides a foundation that can be extended with more advanced retrieval techniques, additional document formats, conversation memory, streaming responses, and deployment capabilities.
