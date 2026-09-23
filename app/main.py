from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router


app = FastAPI(
    title="Local RAG Document Q&A",
    description="Local document Q&A chatbot using Ollama and ChromaDB",
    version="1.0.0"
)


app.include_router(router)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def root():
    return FileResponse(
        "static/index.html"
    )