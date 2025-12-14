import time
import hashlib
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from http_client import get_with_proxy

USER_AGENT = "Mozilla/5.0 (compatible; JobScraperUltimate/1.0)"

class SiteResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def lever_search(keyword: str, location: str, max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """Search Lever job boards via their public search endpoint.
    Many companies host at jobs.lever.co/<company>. We use global search.
    """
    query = f"{keyword} {location}".strip()
    # Lever search page presents a global search
    url = "https://jobs.lever.co/search/?commit=filter&query=" + requests.utils.quote(query)
    headers = {"User-Agent": USER_AGENT}
    if verbose:
        print(f"[lever] GET {url}")
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[lever] error", e)
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    out: List[SiteResult] = []
    for a in soup.select("a.posting-title"):
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        # Company and location nearby
        parent = a.find_parent("div", class_="posting")
        snippet = ""
        if parent:
            comp = parent.select_one("span.posting-company")
            loc = parent.select_one("span.posting-location")
            parts = []
            if comp:
                parts.append(comp.get_text(" ", strip=True))
            if loc:
                parts.append(loc.get_text(" ", strip=True))
            snippet = " | ".join(parts)
        full_url = href if href.startswith("http") else "https://jobs.lever.co" + href
        out.append({
            "engine": "lever",
            "query": query,
            "title": title,
            "url": full_url,
            "snippet": snippet,
            "ts": int(time.time()),
            "hash": _hash(title, full_url)
        })
        if len(out) >= max_results:
            break
    return out
