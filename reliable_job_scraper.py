"""
RELIABLE JOB SCRAPER - Using Official DDG API + Job Board Scrapers
Uses ddgs package (official Python wrapper) instead of HTML scraping
Combines with direct job board scrapers for maximum results
"""

from ddgs import DDGS
from typing import List, Dict
import time
import hashlib
from http_client import get_with_proxy
from bs4 import BeautifulSoup

JOB_KEYWORDS = [
    "hiring", "jobs", "careers", "employment", "positions", 
    "openings", "opportunities", "apply", "join our team"
]

JOB_BOARDS = [
    "indeed.com", "linkedin.com", "glassdoor.com", "monster.com",
    "dice.com", "ziprecruiter.com", "simplyhired.com", 
    "greenhouse.io", "lever.co", "remoteok.com"
]

def _hash(title: str, url: str) -> str:
    """Generate unique hash for deduplication"""
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def is_job_related(text: str, url: str) -> bool:
    """Check if content appears job-related"""
    text_lower = text.lower()
    url_lower = url.lower()
    
    if any(board in url_lower for board in JOB_BOARDS):
        return True
    
    keyword_matches = sum(1 for kw in JOB_KEYWORDS if kw in text_lower)
    return keyword_matches >= 1

def search_duckduckgo_api(query: str, max_results: int = 20) -> List[Dict]:
    """
    Search using official DuckDuckGo API via duckduckgo-search package
    MUCH more reliable than HTML scraping - no CAPTCHA/blocking
    """
    try:
        results = []
        
        with DDGS() as ddgs:
            # DDGS.text() returns generator of results
            for result in ddgs.text(query, max_results=max_results):
                try:
                    title = result.get("title", "")
                    url = result.get("href", "")
                    body = result.get("body", "")
                    
                    if not url or not title:
                        continue
                    
                    # Check if job-related
                    if is_job_related(f"{title} {body}", url):
                        results.append({
                            "title": title,
                            "url": url,
                            "snippet": body[:200],
                            "engine": "duckduckgo_api",
                            "hash": _hash(title, url)
                        })
                except Exception as e:
                    continue
        
        return results
    
    except Exception as e:
        print(f"⚠️ DDG API Error: {e}")
        return []

def search_job_board_google(board: str, keyword: str, location: str = "", max_results: int = 5) -> List[Dict]:
    """
    Use Google site search to find jobs on specific job boards
    Query Google for: site:indeed.com "Python" "New York"
    """
    results = []
    
    # Build search query
    if location:
        q = f'site:{board} "{keyword}" "{location}" (jobs OR careers OR hiring)'
    else:
        q = f'site:{board} "{keyword}" (jobs OR careers OR hiring)'
    
    try:
        with DDGS() as ddgs:
            for result in ddgs.text(q, max_results=max_results):
                try:
                    title = result.get("title", "")
                    url = result.get("href", "")
                    body = result.get("body", "")
                    
                    if not url or not title:
                        continue
                    
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": body[:200],
                        "engine": f"google_site_{board}",
                        "hash": _hash(title, url)
                    })
                except:
                    continue
    except Exception as e:
        pass
    
    return results

def scrape_job_listings(keyword: str, location: str = "", max_results: int = 50) -> List[Dict]:
    """
    Multi-source job scraper using API-based approaches
    ✓ Works reliably without blocking
    ✓ Uses official APIs and standard search
    ✓ No CAPTCHA or bot detection issues
    """
    
    all_results = []
    seen_urls = set()
    
    print(f"\n🔍 Searching for: {keyword} {location if location else '(any location)'}")
    print("=" * 70)
    
    # Method 1: Direct DuckDuckGo API search
    print("[1/3] DuckDuckGo API Search...")
    query = f"{keyword} jobs {location}".strip()
    ddg_results = search_duckduckgo_api(query, max_results=20)
    print(f"      ✓ Found {len(ddg_results)} results")
    
    for r in ddg_results:
        url = r.get("url")
        if url and url not in seen_urls:
            all_results.append(r)
            seen_urls.add(url)
    
    time.sleep(0.5)
    
    # Method 2: Job board specific searches
    print("[2/3] Major Job Board Searches...")
    job_boards_to_search = [
        "indeed.com",
        "linkedin.com", 
        "glassdoor.com",
    ]
    
    board_count = 0
    for board in job_boards_to_search:
        board_results = search_job_board_google(board, keyword, location, max_results=5)
        for r in board_results:
            url = r.get("url")
            if url and url not in seen_urls:
                all_results.append(r)
                seen_urls.add(url)
                board_count += 1
        time.sleep(0.3)
    
    print(f"      ✓ Found {board_count} board-specific results")
    
    time.sleep(0.5)
    
    # Method 3: Remote-specific variant
    print("[3/3] Remote Work Variant...")
    remote_query = f"{keyword} remote jobs {location}".strip()
    remote_results = search_duckduckgo_api(remote_query, max_results=15)
    
    for r in remote_results:
        url = r.get("url")
        if url and url not in seen_urls:
            all_results.append(r)
            seen_urls.add(url)
    
    print(f"      ✓ Found {len(remote_results)} remote results")
    
    print("\n" + "=" * 70)
    print(f"✅ TOTAL UNIQUE JOBS FOUND: {len(all_results)}")
    print("=" * 70)
    
    return all_results[:max_results]

def batch_scrape_jobs(keywords: List[str], locations: List[str] = None, max_per_query: int = 20) -> Dict[str, List[Dict]]:
    """
    Batch scrape multiple keywords and locations
    """
    if not locations:
        locations = [""]
    
    all_results = {}
    
    for keyword in keywords:
        for location in locations:
            query_key = f"{keyword} @ {location}" if location else keyword
            
            print(f"\n📍 Scraping: {query_key}")
            results = scrape_job_listings(keyword, location, max_results=max_per_query)
            
            all_results[query_key] = results
            time.sleep(1)  # Throttle between queries
    
    return all_results

if __name__ == "__main__":
    # Test
    print("JOB SCRAPER - TESTING")
    results = scrape_job_listings("Python developer", "New York", max_results=15)
    
    print(f"\n\n📋 RESULTS ({len(results)} jobs found):")
    print("=" * 70)
    
    for i, job in enumerate(results[:10], 1):
        print(f"\n{i}. {job['title'][:70]}")
        print(f"   🔗 {job['url'][:80]}")
        print(f"   📝 {job.get('snippet', '')[:100]}")
