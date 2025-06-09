import glob
import json
import os
from typing import Dict, List


def prepare_author_list(papers_dir: str = "papers", output_file: str = "authors.json") -> str:
    """Create mapping of author -> affiliation and list of papers."""
    authors: Dict[str, Dict[str, List[str]]] = {}
    for path in glob.glob(os.path.join(papers_dir, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        title = data.get("title")
        for author in data.get("authors", []):
            name = author.get("name")
            if not name:
                continue
            aff = author.get("affiliation") or "Unknown"
            entry = authors.setdefault(name, {"affiliation": aff, "papers": []})
            if not entry.get("affiliation"):
                entry["affiliation"] = aff
            if title and title not in entry["papers"]:
                entry["papers"].append(title)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=2)
    return output_file


if __name__ == "__main__":
    path = prepare_author_list()
    print(f"Author list saved to {path}")
