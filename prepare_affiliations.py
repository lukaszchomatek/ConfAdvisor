import glob
import json
import os
from typing import Dict, List


def prepare_affiliation_list(papers_dir: str = "papers", output_file: str = "affiliations.json") -> str:
    """Create a mapping of affiliation -> list of paper titles."""
    affiliations: Dict[str, List[str]] = {}
    for path in glob.glob(os.path.join(papers_dir, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        title = data.get("title")
        for author in data.get("authors", []):
            aff = author.get("affiliation") or "Unknown"
            affiliations.setdefault(aff, [])
            if title and title not in affiliations[aff]:
                affiliations[aff].append(title)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(affiliations, f, ensure_ascii=False, indent=2)
    return output_file


if __name__ == "__main__":
    path = prepare_affiliation_list()
    print(f"Affiliation list saved to {path}")
