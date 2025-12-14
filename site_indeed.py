import time
import hashlib
from typing import List, Dict
from urllib.parse import urlencode, urljoin
import requests
from bs4 import BeautifulSoup
from http_client import get_with_proxy

USER_AGENT = "Mozilla/5.0 (compatible; JobScraperUltimate/1.0)"
BASE = "https://www.indeed.com/"

class SiteResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def indeed_search(keyword: str, location: str, max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """Scrape Indeed search results for a keyword + location.
    Heuristic HTML parser that attempts multiple selector strategies.
    """
    params = {"q": keyword}
    if location:
        params["l"] = location
    url = urljoin(BASE, f"jobs?{urlencode(params)}")
    headers = {"User-Agent": USER_AGENT}
    if verbose:
        print(f"[indeed] GET {url}")
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[indeed] error", e)
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    out: List[SiteResult] = []

    # Strategy 1: cards with data-jk attribute
    for a in soup.select('a[data-jk]'):
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        if not title or not href:
            continue
        # Find nearby snippet
        snippet = ""
        card = a.find_parent(attrs={"data-jk": True}) or a.find_parent("div")
        if card:
            sn = card.select_one("div.jobSnippet") or card.select_one("ul.job-snippet") or card.select_one("div.slider_container")
            if sn:
                snippet = sn.get_text(" ", strip=True)
        full_url = href if href.startswith("http") else urljoin(BASE, href)
        out.append({
            "engine": "indeed",
            "query": f"{keyword} {location}".strip(),
            "title": title,
            "url": full_url,
            "snippet": snippet,
            "ts": int(time.time()),
            "hash": _hash(title, full_url)
        })
        if len(out) >= max_results:
            return out

    # Strategy 2: classic job links under h2.jobTitle
    for h2 in soup.select("h2.jobTitle"):
        a = h2.find("a")
        if not a:
            continue
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        if not title or not href:
            continue
        snippet = ""
        card = h2.find_parent("div")
        if card:
            sn = card.select_one("div.jobSnippet") or card.select_one("ul.job-snippet")
            if sn:
                snippet = sn.get_text(" ", strip=True)
        full_url = href if href.startswith("http") else urljoin(BASE, href)
        out.append({
            "engine": "indeed",
            "query": f"{keyword} {location}".strip(),
            "title": title,
            "url": full_url,
            "snippet": snippet,
            "ts": int(time.time()),
            "hash": _hash(title, full_url)
        })
        if len(out) >= max_results:
            break

    return out
