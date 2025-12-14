import os
import time
import hashlib
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# Try to use the reliable job scraper if available
try:
    from ddgs import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False

# Try to import LinkedIn scraper
try:
    from site_linkedin import linkedin_job_search
    HAS_LINKEDIN = True
except ImportError:
    HAS_LINKEDIN = False

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Global proxy manager instance (initialized on demand)
_proxy_manager = None

def get_proxy_manager():
    """Get or create proxy manager instance"""
    global _proxy_manager
    if _proxy_manager is None:
        try:
            from proxy_manager import ProxyManager
            _proxy_manager = ProxyManager()
        except ImportError:
            _proxy_manager = None
    return _proxy_manager

class SearchEngineResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

# ===== RELIABLE JOB-FOCUSED SEARCH USING DDGS API =====

JOB_KEYWORDS = ["hiring", "jobs", "careers", "employment", "positions", "openings"]
JOB_BOARDS = [
    "indeed.com", "linkedin.com", "glassdoor.com", "monster.com",
    "dice.com", "ziprecruiter.com", "simplyhired.com", 
    "greenhouse.io", "lever.co", "remoteok.com"
]

def _is_job_result(title: str, body: str, url: str) -> bool:
    """Check if result is likely job-related"""
    text = (title + " " + body).lower()
    url_lower = url.lower()
    
    # Known job board = definitely job result
    if any(board in url_lower for board in JOB_BOARDS):
        return True
    
    # Look for job keywords
    job_kw_count = sum(1 for kw in JOB_KEYWORDS if kw in text)
    return job_kw_count >= 1

def duckduckgo_search_v2(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    """
    NEW: Search using official DDGS API instead of HTML scraping
    ✅ No CAPTCHA blocking
    ✅ No timeout issues  
    ✅ Reliable results
    Falls back to old method if DDGS unavailable
    """
    
    if not HAS_DDGS:
        if verbose:
            print("[duckduckgo_v2] DDGS not available, falling back to HTML scraping")
        return duckduckgo_search(query, max_results, verbose, use_proxy)
    
    if verbose:
        print(f"[duckduckgo_v2] Searching DDGS API for: {query}")
    
    try:
        results = []
        seen_hashes = set()
        
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results * 2):
                try:
                    title = result.get("title", "")
                    url = result.get("href", "")
                    body = result.get("body", "")
                    
                    if not url or not title or len(title) < 3:
                        continue
                    
                    # Deduplicate
                    h = _hash(title, url)
                    if h in seen_hashes:
                        continue
                    seen_hashes.add(h)
                    
                    # Filter for job-related content
                    if _is_job_result(title, body, url):
                        results.append(SearchEngineResult({
                            "title": title,
                            "url": url,
                            "snippet": body[:250],
                            "engine": "duckduckgo_v2",
                            "hash": h
                        }))
                        
                        if len(results) >= max_results:
                            break
                            
                except Exception as e:
                    if verbose:
                        print(f"  [Error parsing result: {e}]")
                    continue
        
        if verbose:
            print(f"[duckduckgo_v2] Found {len(results)} job-related results")
        
        return results
    
    except Exception as e:
        if verbose:
            print(f"[duckduckgo_v2] Error: {e}")
        # Fallback to old method
        return duckduckgo_search(query, max_results, verbose, use_proxy)

# ---------------- DuckDuckGo -----------------

def duckduckgo_search(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    """HTML scrape DuckDuckGo SERP. Uses the regular HTML version."""
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }
    
    if verbose:
        print(f"[duckduckgo] GET {url} q={query}")
    
    # Try with proxy first if enabled, then fallback to no proxy
    proxies = None
    used_proxy = False
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        
        # Try with proxy if enabled
        if use_proxy:
            proxy_mgr = get_proxy_manager()
            if proxy_mgr and proxy_mgr.proxies:
                proxy_dict = proxy_mgr.get_next_proxy()
                if proxy_dict:
                    proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                    if verbose and proxies:
                        print(f"[duckduckgo] Using proxy: {proxy_dict.get('url')}")
                    used_proxy = True
        
        # Try to get cookies first
        session.get("https://duckduckgo.com/", timeout=10, proxies=proxies)
        time.sleep(0.5)
        
        resp = session.get(url, params={"q": query}, timeout=25, proxies=proxies)
        
        # Check for CAPTCHA challenge
        if "confirm this search was made by a human" in resp.text or resp.status_code == 202:
            if verbose:
                print("[duckduckgo] CAPTCHA challenge detected - DuckDuckGo is blocking automated requests")
            return []
        
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[duckduckgo] error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # If proxy failed, retry without proxy
        if used_proxy and use_proxy:
            if verbose:
                print("[duckduckgo] Proxy failed, retrying without proxy...")
            try:
                session = requests.Session()
                session.headers.update(headers)
                
                session.get("https://duckduckgo.com/", timeout=10, proxies=None)
                time.sleep(0.5)
                
                resp = session.get(url, params={"q": query}, timeout=25, proxies=None)
                
                if "confirm this search was made by a human" in resp.text or resp.status_code == 202:
                    if verbose:
                        print("[duckduckgo] CAPTCHA challenge detected - DuckDuckGo is blocking automated requests")
                    return []
                
                resp.raise_for_status()
            except Exception as e2:
                if verbose:
                    print(f"[duckduckgo] error without proxy: {e2}")
                return []
        else:
            return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    out = []
    
    # Find all result links
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        title = link.get_text(strip=True)
        
        # Skip empty titles
        if not title or len(title) < 3:
            continue
        
        # DDG wraps results in //duckduckgo.com/l/?uddg=... - extract actual URL
        if href.startswith("//duckduckgo.com/l/"):
            # Extract the actual URL from the redirect
            import urllib.parse
            try:
                params = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in params:
                    actual_url = params["uddg"][0]
                    href = actual_url
                else:
                    continue
            except:
                continue
        
        # Skip non-http and DDG internal links
        if not href.startswith("http"):
            continue
        if "duckduckgo" in href.lower():
            continue
        
        out.append({
            "engine": "duckduckgo",
            "query": query,
            "title": title,
            "url": href,
            "snippet": "",
            "ts": int(time.time()),
            "hash": _hash(title, href)
        })
        
        if len(out) >= max_results:
            return out
    
    return out

# ---------------- Startpage Search -----------------

def startpage_search(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    """HTML scrape Startpage (privacy-friendly search)."""
    url = "https://www.startpage.com/sp/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    if verbose:
        print(f"[startpage] GET {url} q={query}")
    
    # Try with proxy first if enabled, then fallback to no proxy
    proxies = None
    used_proxy = False
    
    try:
        if use_proxy:
            proxy_mgr = get_proxy_manager()
            if proxy_mgr and proxy_mgr.proxies:
                proxy_dict = proxy_mgr.get_next_proxy()
                if proxy_dict:
                    proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                    if verbose and proxies:
                        print(f"[startpage] Using proxy: {proxy_dict.get('url')}")
                    used_proxy = True
        
        resp = requests.get(url, params={"query": query}, headers=headers, timeout=25, proxies=proxies)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[startpage] error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # If proxy failed, retry without proxy
        if used_proxy and use_proxy:
            if verbose:
                print("[startpage] Proxy failed, retrying without proxy...")
            try:
                resp = requests.get(url, params={"query": query}, headers=headers, timeout=25, proxies=None)
                resp.raise_for_status()
            except Exception as e2:
                if verbose:
                    print(f"[startpage] error without proxy: {e2}")
                return []
        else:
            return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    out = []
    
    # Find result divs with class 'result'
    for result in soup.find_all("div", class_="result"):
        try:
            # Get title and URL from the link
            link = result.find("a", class_="title")
            if not link:
                continue
            
            title = link.get_text(strip=True)
            href = link.get("href", "")
            
            if not title or not href or len(title) < 3:
                continue
            
            # Get snippet if available
            snippet = ""
            snippet_elem = result.find("p", class_="description")
            if snippet_elem:
                snippet = snippet_elem.get_text(strip=True)[:200]
            
            out.append({
                "engine": "startpage",
                "query": query,
                "title": title,
                "url": href,
                "snippet": snippet,
                "ts": int(time.time()),
                "hash": _hash(title, href)
            })
            
            if len(out) >= max_results:
                return out
        except:
            continue
    
    return out

# ---------------- Google Custom Search (stub) -----------------

def google_cse_search(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        if verbose:
            print("[google_cse] missing GOOGLE_API_KEY or GOOGLE_CSE_ID; skipping")
        return []
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query}
    if verbose:
        print(f"[google_cse] GET {endpoint} q={query}")
    
    # Try with proxy first if enabled, then fallback to no proxy
    proxies = None
    used_proxy = False
    
    try:
        if use_proxy:
            proxy_mgr = get_proxy_manager()
            if proxy_mgr and proxy_mgr.proxies:
                proxy_dict = proxy_mgr.get_next_proxy()
                if proxy_dict:
                    proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                    if verbose and proxies:
                        print(f"[google_cse] Using proxy: {proxy_dict.get('url')}")
                    used_proxy = True
        
        resp = requests.get(endpoint, params=params, timeout=30, proxies=proxies)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[google_cse] error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # If proxy failed, retry without proxy
        if used_proxy and use_proxy:
            if verbose:
                print("[google_cse] Proxy failed, retrying without proxy...")
            try:
                resp = requests.get(endpoint, params=params, timeout=30, proxies=None)
                resp.raise_for_status()
            except Exception as e2:
                if verbose:
                    print(f"[google_cse] error without proxy: {e2}")
                return []
        else:
            return []
    
    data = resp.json()
    items = data.get("items", [])
    out = []
    for it in items[:max_results]:
        out.append({
            "engine": "google_cse",
            "query": query,
            "title": it.get("title"),
            "url": it.get("link"),
            "snippet": it.get("snippet", ""),
            "ts": int(time.time()),
            "hash": _hash(it.get("title", ""), it.get("link", ""))
        })
    return out

# ---------------- Bing Web Search (stub) -----------------

def bing_search(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        if verbose:
            print("[bing] missing BING_API_KEY; skipping")
        return []
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    params = {"q": query, "count": max_results}
    headers = {"Ocp-Apim-Subscription-Key": api_key, "User-Agent": USER_AGENT}
    if verbose:
        print(f"[bing] GET {endpoint} q={query}")
    
    # Try with proxy first if enabled, then fallback to no proxy
    proxies = None
    used_proxy = False
    
    try:
        if use_proxy:
            proxy_mgr = get_proxy_manager()
            if proxy_mgr and proxy_mgr.proxies:
                proxy_dict = proxy_mgr.get_next_proxy()
                if proxy_dict:
                    proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                    if verbose and proxies:
                        print(f"[bing] Using proxy: {proxy_dict.get('url')}")
                    used_proxy = True
        
        resp = requests.get(endpoint, params=params, headers=headers, timeout=30, proxies=proxies)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[bing] error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # If proxy failed, retry without proxy
        if used_proxy and use_proxy:
            if verbose:
                print("[bing] Proxy failed, retrying without proxy...")
            try:
                resp = requests.get(endpoint, params=params, headers=headers, timeout=30, proxies=None)
                resp.raise_for_status()
            except Exception as e2:
                if verbose:
                    print(f"[bing] error without proxy: {e2}")
                return []
        else:
            return []
    
    data = resp.json()
    web_pages = data.get("webPages", {}).get("value", [])
    out = []
    for it in web_pages[:max_results]:
        out.append({
            "engine": "bing",
            "query": query,
            "title": it.get("name"),
            "url": it.get("url"),
            "snippet": it.get("snippet", ""),
            "ts": int(time.time()),
            "hash": _hash(it.get("name", ""), it.get("url", ""))
        })
    return out

# ---------------- SerpAPI (robust paid service) -----------------

def serpapi_search(query: str, max_results: int = 20, verbose: bool = False, use_proxy: bool = True) -> List[SearchEngineResult]:
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        if verbose:
            print("[serpapi] missing SERPAPI_KEY; skipping")
        return []
    try:
        from serpapi import GoogleSearch
    except ImportError:
        if verbose:
            print("[serpapi] google-search-results-python not installed; skipping")
        return []
    params = {
        "q": query,
        "api_key": api_key,
        "num": max_results
    }
    if verbose:
        print(f"[serpapi] searching: {query}")
    
    # Try with proxy first if enabled, then fallback to no proxy
    used_proxy = False
    
    try:
        if use_proxy:
            proxy_mgr = get_proxy_manager()
            if proxy_mgr and proxy_mgr.proxies:
                proxy_dict = proxy_mgr.get_next_proxy()
                if proxy_dict:
                    # SerpAPI supports proxy parameter
                    proxy_url = proxy_dict.get('url', '')
                    if proxy_url:
                        params["proxy"] = proxy_url
                        used_proxy = True
                        if verbose:
                            print(f"[serpapi] Using proxy: {proxy_url}")
        
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        if verbose:
            print(f"[serpapi] error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # If proxy failed, retry without proxy
        if used_proxy and use_proxy:
            if verbose:
                print("[serpapi] Proxy failed, retrying without proxy...")
            try:
                # Remove proxy from params and retry
                params_no_proxy = {k: v for k, v in params.items() if k != "proxy"}
                search = GoogleSearch(params_no_proxy)
                results = search.get_dict()
            except Exception as e2:
                if verbose:
                    print(f"[serpapi] error without proxy: {e2}")
                return []
        else:
            return []
    
    
    organic = results.get("organic_results", [])
    out = []
    for it in organic[:max_results]:
        out.append({
            "engine": "serpapi",
            "query": query,
            "title": it.get("title"),
            "url": it.get("link"),
            "snippet": it.get("snippet", ""),
            "ts": int(time.time()),
            "hash": _hash(it.get("title", ""), it.get("link", ""))
        })
    return out

# ============= LINKEDIN JOBS =============

def linkedin_search(query: str, max_results: int = 20, verbose: bool = False, 
                   linkedin_email: str = "", linkedin_password: str = "") -> List[SearchEngineResult]:
    """
    Search LinkedIn for job listings.
    Requires LinkedIn credentials to be provided or loaded from environment.
    """
    
    if not HAS_LINKEDIN:
        if verbose:
            print("[linkedin] site_linkedin module not available")
        return []
    
    try:
        # Use provided credentials or get from environment
        email = linkedin_email or os.getenv("LINKEDIN_EMAIL", "")
        password = linkedin_password or os.getenv("LINKEDIN_PASSWORD", "")
        
        if not email or not password:
            if verbose:
                print("[linkedin] LinkedIn credentials not configured. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in settings.")
            return []
        
        if verbose:
            print(f"[linkedin] Searching for: {query}")
        
        # Extract location if included in query
        location = ""
        if " in " in query.lower():
            parts = query.split(" in ", 1)
            query_term = parts[0].strip()
            location = parts[1].strip() if len(parts) > 1 else ""
        else:
            query_term = query
        
        results_data = linkedin_job_search(
            keyword=query_term,
            location=location,
            email=email,
            password=password,
            max_results=max_results,
            verbose=verbose
        )
        
        # Convert to SearchEngineResult format
        results = []
        for item in results_data:
            try:
                result = SearchEngineResult({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "engine": "linkedin",
                    "company": item.get("company", ""),
                    "location": item.get("location", ""),
                    "hash": item.get("hash", _hash(item.get("title", ""), item.get("url", "")))
                })
                results.append(result)
            except Exception as e:
                if verbose:
                    print(f"[linkedin] Error converting result: {e}")
                continue
        
        if verbose:
            print(f"[linkedin] Found {len(results)} results")
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"[linkedin] Error: {e}")
        return []

ENGINE_FUNCS = {
    "duckduckgo": duckduckgo_search_v2,  # Use new reliable API-based version
    "startpage": startpage_search,
    "google_cse": google_cse_search,
    "bing": bing_search,
    "serpapi": serpapi_search,
    "linkedin": linkedin_search,  # LinkedIn jobs scraper
}

# Note: DuckDuckGo now uses official DDGS API (no blocking!)
# Fallback available to old HTML scraping if DDGS unavailable
# LinkedIn requires credentials in .env file (LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

