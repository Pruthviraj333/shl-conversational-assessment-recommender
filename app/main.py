from fastapi import FastAPI

from app.models.api import ChatRequest
from app.services.chat_service import ChatService

app = FastAPI(
    title="SHL Conversational Assessment Recommender",
    version="1.0.0",
)

service = ChatService()


@app.get("/")
def root():
    return {
        "message": "SHL Conversational Assessment Recommender API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": m.role,
            "content": m.content,
        }
        for m in request.messages
    ]

    return service.chat(messages)