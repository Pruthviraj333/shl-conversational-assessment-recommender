import re
from pathlib import Path

from app.services.chat_service import ChatService

service = ChatService()

TRACE_DIR = Path("sample_conversations")


def parse_users(text):
    pattern = r"\*\*User\*\*\s*> (.*?)(?=\n\n\*\*Agent|\Z)"
    return [m.strip() for m in re.findall(pattern, text, re.S)]


def parse_expected(text):
    urls = re.findall(
        r"https://www\.shl\.com/products/product-catalog/view/([^/]+)/",
        text,
    )
    return sorted(set(urls))


trace_files = sorted(TRACE_DIR.glob("C*.md"))

for trace in trace_files:

    print("\n" + "=" * 90)
    print(trace.name)
    print("=" * 90)

    text = trace.read_text(encoding="utf-8")

    expected = parse_expected(text)

    messages = []

    for user in parse_users(text):

        messages.append(
            {
                "role": "user",
                "content": user,
            }
        )

        response = service.chat(messages)

        print("\nUSER:")
        print(user)

        print("\nBOT:")
        print(response["reply"])

        if response["recommendations"]:

            print("\nOUR RECOMMENDATIONS:")

            for r in response["recommendations"]:
                print("-", r["name"])

        messages.append(
            {
                "role": "assistant",
                "content": response["reply"],
            }
        )

    print("\nEXPECTED PRODUCTS")

    for e in expected:
        print("-", e)

    print()