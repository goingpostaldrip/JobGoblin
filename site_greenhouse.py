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

def greenhouse_search(keyword: str, location: str, max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """Search Greenhouse job boards by keyword. Crawls known public boards via sitemap index.
    This is a heuristic approach: we fetch https://boards.greenhouse.io/ and search results pages.
    """
    headers = {"User-Agent": USER_AGENT}
    query = f"{keyword} {location}".strip()
    url = "https://boards.greenhouse.io/search?q=" + requests.utils.quote(query)
    if verbose:
        print(f"[greenhouse] GET {url}")
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[greenhouse] error", e)
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    out: List[SiteResult] = []
    for job in soup.select(".job"):
        a = job.select_one("a")
        if not a:
            continue
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        company = job.select_one(".company")
        location_el = job.select_one(".location")
        snippet = ""
        if company or location_el:
            parts = []
            if company:
                parts.append(company.get_text(" ", strip=True))
            if location_el:
                parts.append(location_el.get_text(" ", strip=True))
            snippet = " | ".join(parts)
        full_url = href if href.startswith("http") else "https://boards.greenhouse.io" + href
        out.append({
            "engine": "greenhouse",
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
