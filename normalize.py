import re
from urllib.parse import urlparse

def clean_url(u: str) -> str:
    if not u:
        return u
    # Drop tracking query params (basic heuristic)
    parsed = urlparse(u)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return base.rstrip('/')

JOB_HINT_WORDS = [
    "job", "jobs", "career", "careers", "apply", "hiring", "position", "opening", "vacancy", "contract", "freelance"
]

SERVICE_HINT_WORDS = [
    "repair", "support", "maintenance", "painting", "painter", "handyman", "landscaping", "lawn", "it"
]

def relevance_score(title: str, snippet: str, keywords: list[str] | None = None) -> float:
    text = f"{title} {snippet}".lower()
    score = 0.0
    # base hints
    for w in JOB_HINT_WORDS:
        if w in text:
            score += 1.0
    for w in SERVICE_HINT_WORDS:
        if w in text:
            score += 0.8
    # keyword boost
    if keywords:
        for k in keywords:
            k = (k or "").lower().strip()
            if not k:
                continue
            if k in text:
                score += 1.2
    return score

def is_relevant(title: str, snippet: str, keywords: list[str] | None = None, threshold: float = 1.0) -> bool:
    return relevance_score(title, snippet, keywords) >= threshold

def normalize_record(r: dict) -> dict:
    r = dict(r)
    r["url"] = clean_url(r.get("url"))
    return r
