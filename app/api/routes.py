from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.pipeline import RAGPipeline


router = APIRouter()

rag_pipeline = RAGPipeline()


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "RAG API is running"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = rag_pipeline.ask(question)

        sources = []
        seen = set()

        for item in result["sources"]:

            key = (
                item["source"],
                item["page"]
            )

            if key not in seen:
                sources.append({
                    "source": item["source"],
                    "page": item["page"]
                })
                seen.add(key)

        return {
            "answer": result["answer"],
            "sources": sources
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )