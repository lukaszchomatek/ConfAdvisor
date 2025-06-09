import os
import re
import json
import requests


def fetch_paper(url: str) -> str:
    """Pobiera dane artykułu spod podanego URL i zapisuje je w katalogu
    ``papers``.

    Zwraca ścieżkę do zapisanego pliku JSON. Dodatkowo cache'uje surową
    zawartość z r.jina.ai w katalogu ``raw_pages``.
    """

    target_url = f"https://r.jina.ai/{url}"

    # Nazwa pliku cache oparta na adresie URL
    os.makedirs("raw_pages", exist_ok=True)
    raw_slug = re.sub(r"\W+", "_", url.rsplit("/", 1)[-1].lower()).strip("_")[:50]
    raw_path = os.path.join("raw_pages", f"{raw_slug}.txt")

    if os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        print(target_url)
        with requests.get(target_url) as response:
            text = response.text
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(text)

    lines = text.splitlines()

    title = ""
    url_source = ""
    abstract = ""
    authors = []
    presentation = ""

    for i, line in enumerate(lines):
        if not title and line.startswith("Title:"):
            title = line[len("Title:"):].strip()
        if not url_source and line.startswith("URL Source:"):
            url_source = line[len("URL Source:"):].strip()

        if not presentation and line.startswith("**") and " at [" in line:
            match = re.match(r"\*\*(.+?) at \[([^\]]+)\]", line)
            if match:
                presentation = f"{match.group(1).strip()} at {match.group(2).strip()}"

        if "small-avatar" in line:
            after = line.split(")", 1)[1]
            before = after.split("](", 1)[0]
            parts = [p.strip(" #") for p in before.split("#####") if p.strip()]
            if parts:
                name = parts[0]
                affiliation = ", ".join(parts[1:]) if len(parts) > 1 else None
                authors.append({"name": name, "affiliation": affiliation})

        if line.strip().startswith("Abstract") and not abstract:
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            abstract_lines = []
            while j < len(lines) and lines[j].strip() != "":
                abstract_lines.append(lines[j].strip())
                j += 1
            abstract = " ".join(abstract_lines)

    data = {
        "title": title,
        "url": url_source,
        "abstract": abstract,
        "authors": authors,
        "presentation": presentation,
    }

    os.makedirs("papers", exist_ok=True)
    slug = re.sub(r"\W+", "_", title.lower()).strip("_")[:50]
    filename = os.path.join("papers", f"{slug}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filename
