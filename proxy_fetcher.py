"""
Proxy Fetcher - Fetches verified proxies from multiple reliable sources
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class ProxyFetcher:
    """Fetch verified proxies from multiple sources"""
    
    # Multiple proxy APIs for redundancy
    PROXY_SOURCES = {
        "proxyscrape": {
            "url": "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=5000&limit=500&format=text",
            "type": "text",
        },
        "proxifly": {
            "url": "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all.txt",
            "type": "text",
        },
        "speedx": {
            "url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "type": "text",
        },
        "0xarchit": {
            "url": "https://raw.githubusercontent.com/0xarchit/duckduckgo-webscraper/refs/heads/main/proxies.txt",
            "type": "text",
        },
        # Fallback GitHub list
        "proxylist": {
            "url": "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "type": "text",
        },
    }
    
    def __init__(self, cache_duration_minutes=60):
        """
        Initialize ProxyFetcher
        
        Args:
            cache_duration_minutes: How long to cache proxies before refetching
        """
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.last_fetch_time = None
        self.cached_proxies = {}
        self.fetch_timeout = 15
        
    def fetch_proxies(self, limit: Optional[int] = None, source: str = "auto", force_refresh: bool = False) -> List[str]:
        """
        Fetch proxies from best available source
        
        Args:
            limit: Maximum number of proxies to return
            source: Which source to use (auto, proxyscrape, proxifly, speedx, proxylist)
            force_refresh: Force refresh cache
            
        Returns:
            List of proxy URLs
        """
        # Check cache
        cache_key = source or "auto"
        if not force_refresh and self.last_fetch_time and datetime.now() - self.last_fetch_time < self.cache_duration:
            if cache_key in self.cached_proxies:
                proxies = self.cached_proxies[cache_key]
                if limit:
                    return proxies[:limit]
                return proxies

        # Resolve source order
        source_order = [source] if source != "auto" else ["proxyscrape", "0xarchit", "proxifly", "speedx", "proxylist"]

        for src in source_order:
            proxies = self._fetch_from_source(src)
            if proxies:
                self.cached_proxies[cache_key] = proxies
                self.last_fetch_time = datetime.now()
                print(f"[ProxyFetcher] ✓ Fetched {len(proxies)} proxies from {src}")
                if limit:
                    return proxies[:limit]
                return proxies
        
        # If all failed, try cached
        if cache_key in self.cached_proxies:
            print(f"[ProxyFetcher] Using {len(self.cached_proxies[cache_key])} cached proxies")
            proxies = self.cached_proxies[cache_key]
            if limit:
                return proxies[:limit]
            return proxies
        
        print("[ProxyFetcher] ✗ Failed to fetch proxies from all sources")
        return []
    
    def _fetch_from_source(self, source_key: str) -> List[str]:
        """Fetch from a specific source"""
        meta = self.PROXY_SOURCES.get(source_key)
        if not meta:
            return []
        url = meta.get("url")
        if not url:
            return []
        try:
            print(f"[ProxyFetcher] Fetching from {source_key}...")
            resp = requests.get(url, timeout=self.fetch_timeout)
            resp.raise_for_status()
            proxies = []
            for line in resp.text.strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ":" in line:
                    proxies.append(line if line.startswith("http") else f"http://{line}")
            return proxies[:50]
        except Exception as e:
            print(f"[ProxyFetcher] {source_key} failed: {e}")
            return []
    
    def get_mixed_proxies(self, limit: int = 50, force_refresh: bool = False) -> List[Dict[str, str]]:
        """
        Get proxies with metadata
        
        Args:
            limit: Total number of proxies
            force_refresh: Force refresh cache
            
        Returns:
            List of dicts with 'url' and 'type' keys
        """
        proxies = self.fetch_proxies(limit=limit, force_refresh=force_refresh)
        return [{"url": p, "type": "http"} for p in proxies]
    
    def clear_cache(self):
        """Clear cached proxies"""
        self.cached_proxies = {}
        self.last_fetch_time = None
        print("[ProxyFetcher] Cache cleared")


# Convenience functions
_default_fetcher = None

def get_fetcher() -> ProxyFetcher:
    """Get or create default fetcher instance"""
    global _default_fetcher
    if _default_fetcher is None:
        _default_fetcher = ProxyFetcher()
    return _default_fetcher

def fetch_proxies(limit: Optional[int] = None, source: str = "auto", force_refresh: bool = False) -> List[str]:
    """Fetch proxies"""
    return get_fetcher().fetch_proxies(limit=limit, source=source, force_refresh=force_refresh)

def fetch_all_proxies(limit: int = 50) -> List[Dict[str, str]]:
    """Fetch proxies with metadata"""
    return get_fetcher().get_mixed_proxies(limit=limit)


if __name__ == "__main__":
    # Test
    print("Testing ProxyFetcher...")
    fetcher = ProxyFetcher()
    
    proxies = fetcher.fetch_proxies(limit=5)
    print(f"\nFetched {len(proxies)} proxies:")
    for p in proxies:
        print(f"  - {p}")

