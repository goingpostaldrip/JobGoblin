"""
JOB SCRAPER BOTASAURUS - Production-Grade Job Discovery Engine
Uses Botasaurus framework for anti-detection, smart retries, and caching
Handles DuckDuckGo blocking automatically
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote_plus
import time
import re
from typing import List, Dict, Optional
import hashlib
from http_client import get_with_proxy

# Job-specific search terms for better results
JOB_KEYWORDS = [
    "hiring", "jobs", "careers", "employment", "positions", 
    "openings", "opportunities", "apply", "join our team", "now hiring"
]

JOB_BOARDS = [
    "indeed.com", "linkedin.com", "glassdoor.com", "monster.com",
    "dice.com", "ziprecruiter.com", "simplyhired.com", "careerbuilder.com",
    "greenhouse.io", "lever.co", "workday.com", "icims.com",
    "remoteok.com", "weworkremotely.com", "remotive.io", "flexjobs.com"
]

def _hash(title: str, url: str) -> str:
    """Generate unique hash for deduplication"""
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def is_job_related(text: str, url: str) -> bool:
    """Check if content appears job-related"""
    text_lower = text.lower()
    url_lower = url.lower()
    
    # Check if URL is from known job board
    if any(board in url_lower for board in JOB_BOARDS):
        return True
    
    # Check for job keywords in text
    keyword_matches = sum(1 for kw in JOB_KEYWORDS if kw in text_lower)
    return keyword_matches >= 2

def scrape_duckduckgo_html(query: str, max_results: int = 20) -> List[Dict]:
    """
    Scrape DuckDuckGo HTML version
    More reliable than standard DDG, less likely to block
    """
    url = "https://duckduckgo.com/html/"
    
    try:
        # Use proxy for better detection avoidance
        response = get_with_proxy(
            url, 
            params={"q": query},
            use_proxy=True,
            timeout=15,
            verbose=False
        )
        
        if not response or response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Parse DDG results
        for result_elem in soup.select("div.result, tr"):
            if len(results) >= max_results:
                break
            
            try:
                title_elem = result_elem.select_one("a.result__url, a.result-link, a")
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                url = title_elem.get("href", "")
                
                snippet_elem = result_elem.select_one("a.result__snippet, .result__snippet")
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                if not url or not title or len(title) < 3:
                    continue
                
                # Clean up URL if it's a redirect
                if url.startswith("//duckduckgo.com/l/"):
                    import urllib.parse
                    parsed = urllib.parse.urlparse(url)
                    params = urllib.parse.parse_qs(parsed.query)
                    if "uddg" in params:
                        url = params["uddg"][0]
                
                # Check if job-related
                if is_job_related(f"{title} {snippet}", url):
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet[:200],
                        "engine": "duckduckgo_html",
                        "hash": _hash(title, url)
                    })
                    
            except Exception as e:
                continue
        
        return results
    
    except Exception as e:
        return []

def scrape_duckduckgo_lite(query: str, max_results: int = 15) -> List[Dict]:
    """
    Scrape DuckDuckGo Lite (less likely to block)
    Uses native requests with proxy support
    """
    url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
    
    try:
        response = get_with_proxy(url, use_proxy=True, timeout=15, verbose=False)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Parse Lite results (different structure)
        for row in soup.select("tr"):
            if len(results) >= max_results:
                break
            
            try:
                # DuckDuckGo Lite has results in table rows
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue
                
                link_elem = cells[0].find("a")
                if not link_elem:
                    continue
                
                title = link_elem.get_text(strip=True)
                url = link_elem.get("href", "")
                snippet = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                
                if not url or not title or len(title) < 3:
                    continue
                
                # Check if job-related
                if is_job_related(f"{title} {snippet}", url):
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet[:200],
                        "engine": "duckduckgo_lite",
                        "hash": _hash(title, url)
                    })
            except:
                continue
        
        return results
    except Exception as e:
        return []

def search_job_boards_directly(keyword: str, location: str = "", max_results: int = 10) -> List[Dict]:
    """
    Search major job boards directly
    Indeed, LinkedIn, Glassdoor, etc. via site-specific searches
    """
    results = []
    
    job_board_searches = {
        "indeed": f"site:indeed.com {keyword} jobs {location}",
        "linkedin": f"site:linkedin.com/jobs {keyword} {location}",
        "glassdoor": f"site:glassdoor.com {keyword} {location}",
        "monster": f"site:monster.com {keyword} jobs {location}",
    }
    
    for board_name, search_query in job_board_searches.items():
        # Use lite search for job boards
        board_results = scrape_duckduckgo_lite(search_query, max_results=5)
        
        for result in board_results:
            result["board"] = board_name
            results.append(result)
        
        time.sleep(1)  # Rate limiting
    
    return results

def scrape_job_listings(keyword: str, location: str = "", max_results_per_method: int = 20) -> List[Dict]:
    """
    Multi-method job scraper with fallbacks
    Tries multiple search strategies to maximize results
    """
    
    all_results = []
    seen_urls = set()
    
    print(f"\n🔍 Searching for: {keyword} {location if location else '(any location)'}")
    print("=" * 60)
    
    # Method 1: DuckDuckGo Lite (most reliable, no CAPTCHA)
    print("[1/4] Searching DuckDuckGo Lite...")
    lite_results = scrape_duckduckgo_lite(f"{keyword} jobs {location}", max_results=max_results_per_method)
    print(f"      → Found {len(lite_results)} results")
    for r in lite_results:
        url = r.get("url")
        if url and url not in seen_urls:
            all_results.append(r)
            seen_urls.add(url)
    
    time.sleep(1)
    
    # Method 2: Job board direct searches
    print("[2/4] Searching major job boards...")
    board_results = search_job_boards_directly(keyword, location, max_results=8)
    print(f"      → Found {len(board_results)} results")
    for r in board_results:
        url = r.get("url")
        if url and url not in seen_urls:
            all_results.append(r)
            seen_urls.add(url)
    
    time.sleep(1)
    
    # Method 3: Targeted searches with + modifiers
    print("[3/4] Targeted search ('+hiring'/'+ careers')...")
    modifiers = [f"{keyword} +hiring {location}", f"{keyword} +careers {location}"]
    for mod in modifiers:
        mod_results = scrape_duckduckgo_lite(mod, max_results=8)
        for r in mod_results:
            url = r.get("url")
            if url and url not in seen_urls:
                all_results.append(r)
                seen_urls.add(url)
        time.sleep(0.5)
    print(f"      → Found {len([r for r in all_results if r.get('engine') == 'duckduckgo_lite'])} targeted results")
    
    # Method 4: Remote-specific search
    print("[4/4] Remote work variant...")
    remote_query = f"{keyword} remote jobs {location}"
    remote_results = scrape_duckduckgo_lite(remote_query, max_results=10)
    print(f"      → Found {len(remote_results)} results")
    for r in remote_results:
        url = r.get("url")
        if url and url not in seen_urls:
            all_results.append(r)
            seen_urls.add(url)
    
    print("\n" + "=" * 60)
    print(f"✓ Total unique results found: {len(all_results)}")
    print("=" * 60)
    
    return all_results[:max_results_per_method * 3]  # Return best results

# Export for GUI integration
def batch_scrape_jobs(keywords: List[str], locations: List[str] = None, max_per_query: int = 20) -> Dict[str, List[Dict]]:
    """
    Batch scrape multiple keywords and locations
    Returns organized results by keyword
    """
    if not locations:
        locations = [""]
    
    all_results = {}
    
    for keyword in keywords:
        for location in locations:
            query_key = f"{keyword} @ {location}" if location else keyword
            
            print(f"\n📍 Scraping: {query_key}")
            results = scrape_job_listings(keyword, location, max_results_per_method=max_per_query)
            
            all_results[query_key] = results
            time.sleep(2)  # Throttle between queries
    
    return all_results

if __name__ == "__main__":
    # Test
    results = scrape_job_listings("Python developer", "New York", max_results_per_method=10)
    
    print(f"\nTop results:")
    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {r.get('snippet', '')[:100]}")
