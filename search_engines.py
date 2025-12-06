import os
import time
import hashlib
import requests
from typing import List, Dict
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class SearchEngineResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

# ---------------- DuckDuckGo -----------------

def duckduckgo_search(query: str, max_results: int = 20, verbose: bool = False) -> List[SearchEngineResult]:
    """HTML scrape DuckDuckGo SERP. Uses the regular HTML version."""
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    if verbose:
        print(f"[duckduckgo] GET {url} q={query}")
    
    try:
        resp = requests.get(url, params={"q": query}, headers=headers, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[duckduckgo] error", e)
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

def startpage_search(query: str, max_results: int = 20, verbose: bool = False) -> List[SearchEngineResult]:
    """HTML scrape Startpage (privacy-friendly search)."""
    url = "https://www.startpage.com/sp/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    if verbose:
        print(f"[startpage] GET {url} q={query}")
    
    try:
        resp = requests.get(url, params={"query": query}, headers=headers, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[startpage] error", e)
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

def google_cse_search(query: str, max_results: int = 20, verbose: bool = False) -> List[SearchEngineResult]:
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
    try:
        resp = requests.get(endpoint, params=params, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[google_cse] error", e)
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

def bing_search(query: str, max_results: int = 20, verbose: bool = False) -> List[SearchEngineResult]:
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
    try:
        resp = requests.get(endpoint, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        if verbose:
            print("[bing] error", e)
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

def serpapi_search(query: str, max_results: int = 20, verbose: bool = False) -> List[SearchEngineResult]:
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
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        if verbose:
            print("[serpapi] error", e)
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

ENGINE_FUNCS = {
    "duckduckgo": duckduckgo_search,
    "startpage": startpage_search,
    "google_cse": google_cse_search,
    "bing": bing_search,
    "serpapi": serpapi_search,
}

# Note: Only DuckDuckGo and Startpage work without API keys
# Google CSE, Bing, and SerpAPI require configuration in .env file
