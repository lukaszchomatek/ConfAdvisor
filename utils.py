import re
from datetime import datetime
from typing import Optional, List, Dict

# Regular expression to capture date and start time, e.g. "Mon 23 Jun 2025 11:40"
_PRES_RE = re.compile(r"[A-Za-z]{3} \d{1,2} [A-Za-z]{3} \d{4} \d{2}:\d{2}")


def parse_presentation_datetime(presentation: str) -> Optional[datetime]:
    """Parse presentation string into datetime.

    Returns None if parsing fails.
    """
    if not presentation:
        return None
    match = _PRES_RE.search(presentation)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(0), "%a %d %b %Y %H:%M")
    except ValueError:
        return None


def sort_by_presentation(papers: List[Dict]) -> List[Dict]:
    """Return papers sorted by presentation datetime."""
    return sorted(
        papers,
        key=lambda p: parse_presentation_datetime(p.get("presentation", ""))
        or datetime.max,
    )
