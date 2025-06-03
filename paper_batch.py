import time
from typing import List

from fetch_paper import fetch_paper


def fetch_papers_from_file(file_path: str = "papers.txt", limit_per_minute: int = 20) -> List[str]:
    """Fetch all papers listed in the given file respecting the rate limit.

    Each non-empty line in the file should contain a single URL. The function
    calls :func:`fetch_paper` for every URL and returns the list of paths to
    the created JSON files. To avoid exceeding the API rate limit it waits
    ``60 / limit_per_minute`` seconds between calls.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    delay = 60.0 / limit_per_minute if limit_per_minute else 0
    paths = []

    for url in urls:
        paths.append(fetch_paper(url))
        if delay:
            time.sleep(delay)
    return paths
