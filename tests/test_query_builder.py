from app.services.conversation_analyzer import ConversationAnalyzer
from app.utils.query_builder import QueryBuilder

messages = [
    {
        "role": "user",
        "content": "Hiring Java developer"
    },
    {
        "role": "assistant",
        "content": "What seniority?"
    },
    {
        "role": "user",
        "content": "Senior"
    },
    {
        "role": "assistant",
        "content": "Need personality?"
    },
    {
        "role": "user",
        "content": "Yes add leadership personality"
    }
]

analyzer = ConversationAnalyzer()

state = analyzer.build_state(messages)

query = QueryBuilder.build(
    messages,
    state,
)

print(query)