"""
WeWorkRemotely job scraper - RSS-based, minimal blocking
"""
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

def weworkremotely_search(keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """
    Scrape WeWorkRemotely using their RSS feed
    RSS is less likely to be blocked than HTML scraping
    """
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    
    headers = {"User-Agent": USER_AGENT}
    keyword_lower = keyword.lower()
    out: List[SiteResult] = []
    
    if verbose:
        print(f"[weworkremotely] GET {url}")
    
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[weworkremotely] error: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, 'html.parser')  # Use html parser
    
    # Find all job items in RSS
    items = soup.find_all('item')
    
    for item in items:
        if len(out) >= max_results:
            break
        
        title_elem = item.find('title')
        link_elem = item.find('link')
        desc_elem = item.find('description')
        
        if not title_elem or not link_elem:
            continue
        
        title = title_elem.get_text(strip=True)
        url = link_elem.get_text(strip=True)
        description = desc_elem.get_text(strip=True) if desc_elem else ""
        
        # Filter by keyword
        if keyword_lower not in title.lower() and keyword_lower not in description.lower():
            continue
        
        snippet = description[:200] if description else ""
        
        out.append({
            "engine": "weworkremotely",
            "query": keyword,
            "title": title,
            "url": url,
            "snippet": snippet,
            "ts": int(time.time()),
            "hash": _hash(title, url)
        })
    
    if verbose:
        print(f"[weworkremotely] found {len(out)} results")
    
    return out
