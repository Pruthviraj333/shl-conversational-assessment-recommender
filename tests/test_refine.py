from app.services.chat_service import ChatService

service = ChatService()

messages = [
    {
        "role": "user",
        "content": "Hiring graduate software engineers"
    },
    {
        "role": "assistant",
        "content": "Here are some assessments."
    },
    {
        "role": "user",
        "content": "Actually add personality assessment."
    }
]

response = service.chat(messages)

print(response)