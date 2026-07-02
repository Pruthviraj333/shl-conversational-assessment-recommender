from app.prompts.base_prompt import SYSTEM_PROMPT


def build_refine_prompt(
    messages,
    retrieved_assessments,
):

    conversation = ""

    for message in messages:

        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    context = ""

    for item in retrieved_assessments:

        context += f"""
Name:
{item['name']}

Type:
{item['test_type']}

Category:
{item['keys']}

Description:
{item['meta_description']}

URL:
{item['url']}

--------------------------------
"""

    return f"""
{SYSTEM_PROMPT}

Conversation

{conversation}

Retrieved SHL Assessments

{context}

Task

The user is modifying a previous recommendation.

Update the shortlist using ONLY the retrieved SHL assessments.

Rules

- Respect additions.
- Respect removals.
- Respect replacements.
- Never invent assessment names.
- Never invent URLs.
- Return between 1 and 10 assessments.
- Every recommendation MUST exist in Retrieved SHL Assessments.
- Return ONLY JSON.

Required JSON

{{
    "reply":"",
    "recommendations":[
        {{
            "name":"",
            "url":"",
            "test_type":""
        }}
    ],
    "end_of_conversation":false
}}
"""