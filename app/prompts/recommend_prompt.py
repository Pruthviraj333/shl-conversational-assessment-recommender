from app.prompts.base_prompt import SYSTEM_PROMPT


def build_recommend_prompt(messages, retrieved_assessments):

    conversation = ""

    for message in messages:
        conversation += f"{message['role']}: {message['content']}\n"

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

-------------------------
"""

    prompt = f"""
{SYSTEM_PROMPT}

Conversation

{conversation}

Retrieved SHL Assessments

{context}

Task

Recommend between 1 and 10 SHL assessments.

Rules

- Use ONLY the retrieved assessments provided above.
- Never invent assessment names.
- Never invent URLs.
- Every recommendation must exactly match one assessment from the retrieved context.
- Recommendations must contain ONLY these fields:
  - name
  - url
  - test_type
- If the user's request includes multiple requirements (e.g. technical skills and leadership), try to cover each requirement with one or more assessments from the retrieved context.
- Prefer a balanced shortlist rather than recommending multiple assessments that measure the same capability.
- Assume sufficient information has already been collected.
- Recommend the best matching assessments from the retrieved context.
- Do not ask clarification questions unless the conversation explicitly asks for clarification.
- Return ONLY valid JSON.
- Do NOT wrap the response in markdown.
- Do NOT include explanations before or after the JSON.

Required JSON Schema

{{
  "reply": "",
  "recommendations": [
    {{
      "name": "",
      "url": "",
      "test_type": ""
    }}
  ],
  "end_of_conversation": false
}}
"""

    return prompt