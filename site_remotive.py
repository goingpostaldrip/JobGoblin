"""
Remotive.io job scraper - API-based, developer-friendly
"""
import time
import hashlib
from typing import List, Dict
import requests
from http_client import get_with_proxy

USER_AGENT = "Mozilla/5.0 (compatible; JobScraperUltimate/1.0)"

class SiteResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def remotive_search(keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """
    Scrape Remotive.io using their public API
    Remotive has a free API that doesn't require authentication
    """
    url = "https://remotive.com/api/remote-jobs"
    headers = {"User-Agent": USER_AGENT}
    
    if verbose:
        print(f"[remotive] GET {url}")
    
    try:
        resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        if verbose:
            print(f"[remotive] error: {e}")
        return []
    
    out: List[SiteResult] = []
    keyword_lower = keyword.lower()
    
    jobs = data.get('jobs', [])
    
    for job in jobs:
        if len(out) >= max_results:
            break
        
        title = job.get('title', '')
        company = job.get('company_name', '')
        category = job.get('category', '')
        
        # Filter by keyword
        matches = (
            keyword_lower in title.lower() or
            keyword_lower in company.lower() or
            keyword_lower in category.lower()
        )
        
        if not matches:
            continue
        
        job_url = job.get('url', '')
        description = job.get('description', '')[:200]  # First 200 chars
        
        out.append({
            "engine": "remotive",
            "query": keyword,
            "title": f"{title} at {company}",
            "url": job_url,
            "snippet": description,
            "ts": int(time.time()),
            "hash": _hash(title, job_url)
        })
    
    if verbose:
        print(f"[remotive] found {len(out)} results")
    
    return out
