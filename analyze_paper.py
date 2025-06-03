import json
from typing import Dict
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert in analyzing scientific publications. Your task is to extract, based on the title, URL, and abstract of a conference paper, the most important information in the given JSON format.

Always respond exclusively in the following format. Fill in each field based on the input data, or write null if the information is not present.

Response format:

{
  "title": "...",
  "session": "...",
  "url": "...",
  "keywords": ["...", "...", "..."],
  "domain": "...",
  "problem": "...",
  "solution": "...",
  "results": "...",
  "conclusion": "...",
  "tools": ["..."],
  "evaluation": "..."
}

Field definitions:
- "title": the paper title (shorten, remove the name of the conference/session)
- "session": session name (e.g., "Industry Papers"), extract from the title or URL
- "url": unchanged
- "keywords": 3–5 keywords summarizing the paper's topic
- "domain": 2–5 words, the main field(s) of the article
- "problem": main research/practical problem of the paper
- "solution": main solution/method/system
- "results": the most important numbers, effects, achievements
- "conclusion": practical/scientific significance of the paper
- "tools": names of tools/frameworks if mentioned
- "evaluation": method of evaluation (e.g., experiments, case studies, real data)

Respond with JSON only, without comments or additional explanations.
"""

def analyze_paper(file_path: str) -> str:
    """Augment JSON file with data extracted from GPT-4o (OpenAI Python client v1).

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
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Odpowiedź jest w response.choices[0].message.content
    content = response.choices[0].message.content
    analysis = json.loads(content)

    data.update(analysis)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path
