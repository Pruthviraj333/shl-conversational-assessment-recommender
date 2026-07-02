from fastapi import FastAPI
from pydantic import BaseModel

from app.services.chat_service import ChatService

app = FastAPI(
    title="SHL Assessment Recommender"
)

service = ChatService()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


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