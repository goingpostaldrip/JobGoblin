"""
RemoteOK job scraper - API-based, less blocking
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

def remoteok_search(keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[SiteResult]:
    """
    Scrape RemoteOK using their JSON API
    RemoteOK is API-friendly and doesn't block as aggressively
    """
    url = "https://remoteok.com/api"
    headers = {"User-Agent": USER_AGENT}
    
    if verbose:
        print(f"[remoteok] GET {url}")
    
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            resp = get_with_proxy(url, headers=headers, timeout=30, use_proxy=True, verbose=verbose)
            resp.raise_for_status()
            data = resp.json()
            break
        except Exception as e:
            if verbose:
                print(f"[remoteok] error (attempt {attempts+1}):", e)
            # Try direct request if proxy fails
            if attempts == 0:
                try:
                    resp = requests.get(url, headers=headers, timeout=30)
                    resp.raise_for_status()
                    data = resp.json()
                    break
                except Exception as e2:
                    if verbose:
                        print(f"[remoteok] direct request error (attempt {attempts+1}):", e2)
            # Adjust headers and retry
            headers["User-Agent"] = USER_AGENT + f" Retry{attempts+1}"
            attempts += 1
    else:
        return []
    
    out: List[SiteResult] = []
    keyword_lower = keyword.lower()
    
    # Skip first item (it's metadata)
    for job in data[1:]:
        if len(out) >= max_results:
            break
        title = job.get('position', '')
        company = job.get('company', '')
        tags = job.get('tags', [])
        # Accept all jobs, no keyword filter
        # Build result
        job_url = job.get('url', '')
        if job_url and not job_url.startswith('http'):
            job_url = f"https://remoteok.com{job_url}"
        
        description = job.get('description', '')[:200]  # First 200 chars
        
        out.append({
            "engine": "remoteok",
            "query": keyword,
            "title": f"{title} at {company}",
            "url": job_url,
            "snippet": description,
            "ts": int(time.time()),
            "hash": _hash(title, job_url)
        })
    
    if verbose:
        print(f"[remoteok] found {len(out)} results")
    
    return out
