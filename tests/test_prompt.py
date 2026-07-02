from app.prompts.recommend_prompt import build_recommend_prompt
from app.llm.gemini_client import GeminiClient

messages = [
    {
        "role": "user",
        "content": "Hiring a Java developer with leadership skills."
    }
]

retrieved = [
    {
        "name": "Core Java (Advanced Level) (New)",
        "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
        "test_type": "K",
        "keys": "Knowledge & Skills",
        "meta_description": "Java programming assessment."
    },
    {
        "name": "OPQ Leadership Report",
        "url": "https://www.shl.com/products/product-catalog/view/opq-leadership-report/",
        "test_type": "P",
        "keys": "Personality & Behavior",
        "meta_description": "Leadership personality report."
    }
]

prompt = build_recommend_prompt(
    messages,
    retrieved,
)

client = GeminiClient()

response = client.generate(prompt)

print(response)