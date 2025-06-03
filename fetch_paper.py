import os
import re
import json
import requests


def fetch_paper(url: str) -> str:
    """Pobiera dane artykułu spod podanego URL i zapisuje je w katalogu `papers`.

    Zwraca ścieżkę do zapisanego pliku JSON.
    """
    target_url = f"https://r.jina.ai/{url}"
    print(target_url)
    with requests.get(target_url) as response:
        text = response.text
    lines = text.splitlines()

    title = ""
    url_source = ""
    abstract = ""

    for i, line in enumerate(lines):
        if not title and line.startswith("Title:"):
            title = line[len("Title:"):].strip()
        if not url_source and line.startswith("URL Source:"):
            url_source = line[len("URL Source:"):].strip()
        if line.strip().startswith("Abstract"):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            abstract_lines = []
            while j < len(lines) and lines[j].strip() != "":
                abstract_lines.append(lines[j].strip())
                j += 1
            abstract = " ".join(abstract_lines)
            break

    data = {
        "title": title,
        "url": url_source,
        "abstract": abstract,
    }

    os.makedirs("papers", exist_ok=True)
    slug = re.sub(r"\W+", "_", title.lower()).strip("_")[:50]
    filename = os.path.join("papers", f"{slug}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename
