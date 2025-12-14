import time
import hashlib
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
from http_client import get_with_proxy

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class SiteResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def simplyhired_search(keyword: str, location: str, max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """Search SimplyHired (free job board, no API required)."""
    query = f"{keyword} {location}".strip()
    # SimplyHired uses simple URL structure
    base = "https://www.simplyhired.com/search"
    params = f"q={quote_plus(keyword)}&l={quote_plus(location)}" if location else f"q={quote_plus(keyword)}"
    url = f"{base}?{params}"
    headers = {"User-Agent": USER_AGENT}
    
    if verbose:
        print(f"[simplyhired] GET {url}")
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[simplyhired] error", e)
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    out: List[SiteResult] = []
    
    # Try multiple selector strategies
    for article in soup.select("article.job-listing, div[data-job-id], li.job"):
        title_el = article.select_one("h3 a, h2 a, a.card-link")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        
        # Get snippet/company
        snippet_parts = []
        company = article.select_one(".company, .jobposting-company")
        if company:
            snippet_parts.append(company.get_text(strip=True))
        loc_el = article.select_one(".location, .jobposting-location")
        if loc_el:
            snippet_parts.append(loc_el.get_text(strip=True))
        snippet = " | ".join(snippet_parts)
        
        full_url = href if href.startswith("http") else urljoin("https://www.simplyhired.com", href)
        
        out.append({
            "engine": "simplyhired",
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
