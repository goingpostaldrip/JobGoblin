"""
ULTIMATE JOB SCRAPER - Multi-Strategy Aggressive Job Hunter
Combines DuckDuckGo Lite scraping, proxy rotation, and multiple search angles
Based on 0xarchit/duckduckgo-webscraper with job-specific enhancements
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse, parse_qs, unquote, urljoin, quote_plus
from typing import List, Dict, Optional
import hashlib
from http_client import get_with_proxy

# Job-specific search terms to maximize results
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

def extract_clean_text(html):
    """Extract clean text from HTML"""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 
                      'form', 'img', 'noscript', 'iframe', 'button', 'input']):
        tag.decompose()
    
    text = soup.get_text(separator='\n').strip()
    text = re.sub(r'[\n\s]+', ' ', text)
    return text

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

def scrape_duckduckgo_lite(query: str, max_results: int = 10, use_proxy: bool = True, verbose: bool = False) -> List[Dict]:
    """
    Scrape DuckDuckGo Lite with aggressive proxy rotation
    Uses lite.duckduckgo.com which is less likely to block
    """
    encoded_query = quote_plus(query)
    search_url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
    
    if verbose:
        print(f"[DDG_LITE] Searching: {query}")
    
    try:
        resp = get_with_proxy(
            search_url,
            use_proxy=use_proxy,
            retry_without_proxy=True,
            timeout=20,
            verbose=verbose
        )
        resp.raise_for_status()
        
        if verbose:
            print(f"[DDG_LITE] Got response: {len(resp.text)} bytes")
        
        time.sleep(2)  # Rate limit
        
    except Exception as e:
        if verbose:
            print(f"[DDG_LITE] Error: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    
    # Parse DDG Lite results
    for a in soup.select("a.result-link"):
        if len(results) >= max_results:
            break
            
        title = a.get_text(strip=True)
        raw_link = a.get('href', '')
        
        # Skip ads and help pages
        if 'y.js' in raw_link or 'duckduckgo-help-pages' in raw_link:
            continue
        
        # Decode DuckDuckGo redirect link
        real_url = raw_link
        if "duckduckgo.com/l/?" in raw_link and "uddg=" in raw_link:
            try:
                parsed = urlparse(raw_link)
                query_params = parse_qs(parsed.query)
                real_url = unquote(query_params.get('uddg', [''])[0])
                if real_url.startswith("//"):
                    real_url = "https:" + real_url
            except:
                pass
        
        if not real_url or not title:
            continue
        
        results.append({
            "engine": "duckduckgo_lite",
            "query": query,
            "title": title,
            "url": real_url,
            "snippet": "",
            "ts": int(time.time()),
            "hash": _hash(title, real_url)
        })
    
    if verbose:
        print(f"[DDG_LITE] Found {len(results)} results")
    
    return results

def scrape_duckduckgo_html(query: str, max_results: int = 10, use_proxy: bool = True, verbose: bool = False) -> List[Dict]:
    """
    Scrape DuckDuckGo HTML version (regular)
    Complementary to Lite version for maximum coverage
    """
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    if verbose:
        print(f"[DDG_HTML] Searching: {query}")
    
    try:
        resp = get_with_proxy(
            url,
            params={"q": query},
            headers=headers,
            use_proxy=use_proxy,
            retry_without_proxy=True,
            timeout=20,
            verbose=verbose
        )
        resp.raise_for_status()
        
        time.sleep(2)
        
    except Exception as e:
        if verbose:
            print(f"[DDG_HTML] Error: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    
    for link in soup.find_all("a", href=True):
        if len(results) >= max_results:
            break
            
        href = link.get("href", "")
        title = link.get_text(strip=True)
        
        if not title or len(title) < 3:
            continue
        
        # Parse DuckDuckGo redirect links
        if href.startswith("//duckduckgo.com/l/"):
            try:
                parsed = urlparse(href)
                params = parse_qs(parsed.query)
                if "uddg" in params:
                    actual_url = params["uddg"][0]
                    results.append({
                        "engine": "duckduckgo_html",
                        "query": query,
                        "title": title,
                        "url": actual_url,
                        "snippet": "",
                        "ts": int(time.time()),
                        "hash": _hash(title, actual_url)
                    })
            except:
                continue
    
    if verbose:
        print(f"[DDG_HTML] Found {len(results)} results")
    
    return results

def ultra_job_search(
    keyword: str,
    location: str = "",
    max_results_per_strategy: int = 20,
    use_proxy: bool = True,
    verbose: bool = False
) -> List[Dict]:
    """
    ULTRA-AGGRESSIVE job search using multiple strategies
    
    Strategies:
    1. Direct keyword + location search (DDG Lite)
    2. Direct keyword + location search (DDG HTML)
    3. Keyword + "jobs" + location (DDG Lite)
    4. Keyword + "careers" + location (DDG HTML)
    5. Keyword + "hiring" + location (DDG Lite)
    6. Keyword + location + each major job board (targeted)
    7. Keyword + "remote" if location not specified
    
    All strategies use proxy rotation for maximum success
    """
    all_results = []
    seen_hashes = set()
    
    # Build base query
    base_query = f"{keyword} {location}".strip()
    
    # Strategy 1: DDG Lite - Direct search
    if verbose:
        print(f"\n=== STRATEGY 1: DDG Lite Direct ===")
    results = scrape_duckduckgo_lite(base_query, max_results_per_strategy, use_proxy, verbose)
    for r in results:
        if r['hash'] not in seen_hashes:
            seen_hashes.add(r['hash'])
            all_results.append(r)
    
    time.sleep(3)  # Rate limit between strategies
    
    # Strategy 2: DDG HTML - Direct search
    if verbose:
        print(f"\n=== STRATEGY 2: DDG HTML Direct ===")
    results = scrape_duckduckgo_html(base_query, max_results_per_strategy, use_proxy, verbose)
    for r in results:
        if r['hash'] not in seen_hashes:
            seen_hashes.add(r['hash'])
            all_results.append(r)
    
    time.sleep(3)
    
    # Strategy 3: DDG Lite - "jobs" variant
    if verbose:
        print(f"\n=== STRATEGY 3: DDG Lite + 'jobs' ===")
    jobs_query = f"{keyword} jobs {location}".strip()
    results = scrape_duckduckgo_lite(jobs_query, max_results_per_strategy, use_proxy, verbose)
    for r in results:
        if r['hash'] not in seen_hashes:
            seen_hashes.add(r['hash'])
            all_results.append(r)
    
    time.sleep(3)
    
    # Strategy 4: DDG HTML - "careers" variant
    if verbose:
        print(f"\n=== STRATEGY 4: DDG HTML + 'careers' ===")
    careers_query = f"{keyword} careers {location}".strip()
    results = scrape_duckduckgo_html(careers_query, max_results_per_strategy, use_proxy, verbose)
    for r in results:
        if r['hash'] not in seen_hashes:
            seen_hashes.add(r['hash'])
            all_results.append(r)
    
    time.sleep(3)
    
    # Strategy 5: DDG Lite - "hiring" variant
    if verbose:
        print(f"\n=== STRATEGY 5: DDG Lite + 'hiring' ===")
    hiring_query = f"{keyword} hiring {location}".strip()
    results = scrape_duckduckgo_lite(hiring_query, max_results_per_strategy, use_proxy, verbose)
    for r in results:
        if r['hash'] not in seen_hashes:
            seen_hashes.add(r['hash'])
            all_results.append(r)
    
    time.sleep(3)
    
    # Strategy 6: Targeted job board searches (top 5 boards)
    top_boards = ["indeed", "linkedin", "glassdoor", "monster", "dice"]
    for board in top_boards:
        if len(all_results) >= max_results_per_strategy * 5:
            break
            
        if verbose:
            print(f"\n=== STRATEGY 6.{top_boards.index(board)+1}: {board.title()} Targeted ===")
        
        board_query = f"{keyword} {location} site:{board}.com".strip()
        results = scrape_duckduckgo_lite(board_query, 10, use_proxy, verbose)
        for r in results:
            if r['hash'] not in seen_hashes:
                seen_hashes.add(r['hash'])
                all_results.append(r)
        
        time.sleep(2)
    
    # Strategy 7: Remote variant if no location
    if not location:
        if verbose:
            print(f"\n=== STRATEGY 7: Remote Jobs ===")
        remote_query = f"{keyword} remote jobs"
        results = scrape_duckduckgo_lite(remote_query, max_results_per_strategy, use_proxy, verbose)
        for r in results:
            if r['hash'] not in seen_hashes:
                seen_hashes.add(r['hash'])
                all_results.append(r)
    
    if verbose:
        print(f"\n=== TOTAL RESULTS: {len(all_results)} unique jobs found ===")
    
    return all_results

# Compatibility function for existing code
def duckduckgo_search_jobs(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[Dict]:
    """
    Enhanced DuckDuckGo search specifically optimized for job hunting
    Drop-in replacement for original duckduckgo_search with job enhancements
    """
    # Parse query for keyword/location if formatted as "keyword location"
    parts = query.rsplit(' ', 1)
    if len(parts) == 2 and len(parts[1]) < 30:  # Assume last part might be location
        keyword, location = parts
    else:
        keyword = query
        location = ""
    
    return ultra_job_search(keyword, location, max_results, use_proxy, verbose)

if __name__ == "__main__":
    # Test the scraper
    print("🚀 ULTRA JOB SCRAPER TEST\n")
    
    results = ultra_job_search(
        keyword="Python developer",
        location="remote",
        max_results_per_strategy=5,
        use_proxy=True,
        verbose=True
    )
    
    print(f"\n✅ Found {len(results)} total unique job listings")
    print("\nSample results:")
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['url']}")
