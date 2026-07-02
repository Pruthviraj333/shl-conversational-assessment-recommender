from app.prompts.base_prompt import SYSTEM_PROMPT


def build_compare_prompt(
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

Duration:
{item['duration']}

Description:
{item['meta_description']}

URL:
{item['url']}

------------------------------------------
"""

    return f"""
{SYSTEM_PROMPT}

Conversation

{conversation}

Retrieved SHL Assessments

{context}

Task

The user wants to compare SHL assessments.

Rules

- Compare ONLY assessments from the retrieved context.
- Do NOT use outside knowledge.
- Highlight:
  - Purpose
  - Assessment category
  - When each assessment is appropriate
- Do NOT invent any information.
- Return ONLY JSON.

Required JSON

{{
    "reply":"",
    "recommendations":[],
    "end_of_conversation":false
}}
"""