import json
from typing import Dict
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert analyst focusing on responsible AI and intellectual property. Based on the title, URL, and
abstract of a conference paper, identify potential ethical implications of AI usage and copyright considerations.

Always respond exclusively in the following JSON format. Populate each field based on the input data, or write null (or
an empty array where appropriate) if the information is not present or cannot be inferred.

Response format:

{
  \"title\": \"...\",
  \"url\": \"...\",
  \"ai_usage_summary\": \"...\",
  \"ethical_implications\": [\"...\", \"...\"],
  \"ethical_risk_level\": \"low|medium|high\",
  \"ethical_mitigation\": \"...\",
  \"copyright_implications\": [\"...\", \"...\"],
  \"copyright_risk_level\": \"low|medium|high\",
  \"copyright_mitigation\": \"...\",
  \"additional_notes\": \"...\",
  \"confidence\": \"low|medium|high\"
}

Field definitions:
- \"title\" and \"url\": echo from the input to help cross-reference results.
- \"ai_usage_summary\": brief explanation of how AI is (or could be) used in the described work; null if unrelated.
- \"ethical_implications\": list of possible ethical issues concerning AI usage (bias, misuse, transparency, etc.).
- \"ethical_risk_level\": overall severity of ethical concerns inferred from the abstract.
- \"ethical_mitigation\": mitigation strategies mentioned or recommended; null if none.
- \"copyright_implications\": list of possible copyright or licensing concerns (data ownership, generated content rights, etc.).
- \"copyright_risk_level\": severity of copyright concerns.
- \"copyright_mitigation\": mitigations mentioned or recommended; null if none.
- \"additional_notes\": optional clarifications; null if nothing notable.
- \"confidence\": how confident you are in the assessment given the abstract (low, medium, or high).

Respond with JSON only, without comments or additional explanations.
"""


def analyze_ethics(file_path: str) -> str:
    """Augment JSON file with ethics and copyright analysis extracted via GPT-4o (OpenAI Python client v1).

    The OpenAI API key should be stored in ``key.txt`` in the current working directory.
    Returns the path to the updated file.
    """
    with open("key.txt", "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    client = OpenAI(api_key=api_key)

    with open(file_path, "r", encoding="utf-8") as f:
        data: Dict[str, object] = json.load(f)

    message = {
        "title": data.get("title"),
        "url": data.get("url"),
        "abstract": data.get("abstract"),
    }

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(message, ensure_ascii=False)},
        ],
        response_format={"type": "text"},
        temperature=0,
        max_tokens=768,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    content = response.choices[0].message.content
    analysis = json.loads(content)

    data.update({
        "ethics_analysis": analysis,
    })
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path
