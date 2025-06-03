import json
from typing import Dict

import openai

SYSTEM_PROMPT = """Jesteś ekspertem od analizy publikacji naukowych. Twoim zadaniem jest wyciąganie, na podstawie tytułu, adresu URL i abstraktu artykułu konferencyjnego, najważniejszych informacji w podanym formacie JSON.

Zawsze odpowiadaj wyłącznie w poniższym formacie. Wypełnij każde pole na podstawie danych wejściowych lub wpisz null, jeśli informacja nie występuje.

Format odpowiedzi:

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

Definicje pól:
- "title": tytuł pracy (skróć, usuń nazwę konferencji/sesji)
- "session": nazwę sesji (np. "Industry Papers"), wyciągnij z tytułu lub url
- "url": bez zmian
- "keywords": 3–5 słów kluczowych podsumowujących temat pracy
- "domain": 2–5 słów, główna dziedzina/dziedziny artykułu
- "problem": główny problem badawczy/praktyczny artykułu
- "solution": główne rozwiązanie/metoda/system
- "results": najważniejsze liczby, efekty, osiągnięcia
- "conclusion": praktyczne/naukowe znaczenie pracy
- "tools": nazwy narzędzi, frameworków, jeśli wymieniono
- "evaluation": sposób ewaluacji (np. eksperymenty, studia przypadków, dane rzeczywiste)

Odpowiadaj tylko JSON’em, bez komentarzy ani dodatkowych wyjaśnień.
"""


def analyze_paper(file_path: str) -> str:
    """Augment JSON file with data extracted from GPT-4o.

    The OpenAI API key should be stored in ``key.txt`` in the current
    working directory. The function returns the path to the updated file.
    """
    with open("key.txt", "r", encoding="utf-8") as f:
        openai.api_key = f.read().strip()

    with open(file_path, "r", encoding="utf-8") as f:
        data: Dict[str, object] = json.load(f)

    message = {
        "title": data.get("title"),
        "url": data.get("url"),
        "abstract": data.get("abstract"),
    }

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(message, ensure_ascii=False)},
        ],
        temperature=0,
    )

    content = response["choices"][0]["message"]["content"]
    analysis = json.loads(content)

    data.update(analysis)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path
