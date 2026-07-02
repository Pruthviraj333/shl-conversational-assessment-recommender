from app.services.chat_service import ChatService

service = ChatService()

messages = [
    {
        "role": "user",
        "content": "I'm hiring a Java developer with leadership skills."
    }
]

response = service.chat(messages)

print(response)