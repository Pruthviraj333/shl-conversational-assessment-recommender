from app.services.chat_service import ChatService

service = ChatService()

messages = [
    {
        "role": "user",
        "content": "What is the difference between OPQ and GSA?"
    }
]

response = service.chat(messages)

print(response)