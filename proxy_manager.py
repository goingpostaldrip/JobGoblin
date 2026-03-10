"""
Proxy rotation manager for bypassing rate limiting and blocks
"""
import os
import json
from typing import List, Dict, Optional
from datetime import datetime

# Try to import ProxyFetcher for automatic proxy discovery
try:
    from proxy_fetcher import ProxyFetcher
    HAS_PROXY_FETCHER = True
except ImportError:
    HAS_PROXY_FETCHER = False

class ProxyManager:
    """Manages proxy rotation for web scraping"""
    
    def __init__(self, config_file: str = "proxies.json"):
        self.config_file = config_file
        self.proxies: List[Dict] = []
        self.current_proxy_idx = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.proxies = data.get('proxies', [])
                    print(f"[ProxyManager] Loaded {len(self.proxies)} proxies")
            except Exception as e:
                print(f"[ProxyManager] Error loading proxies: {e}")
                self.proxies = []
        else:
            self.proxies = []
    
    def save_proxies(self):
        """Save proxies to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'proxies': self.proxies,
                    'updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"[ProxyManager] Error saving proxies: {e}")
    
    def add_proxy(self, proxy_url: str, proxy_type: str = "http", username: str = "", password: str = ""):
        """
        Add a proxy
        
        Examples:
        - add_proxy("http://123.45.67.89:8080")
        - add_proxy("http://123.45.67.89:8080", username="user", password="pass")
        - add_proxy("socks5://123.45.67.89:1080")
        """
        if not proxy_url:
            return False
        
        proxy_entry = {
            'url': proxy_url,
            'type': proxy_type,
            'username': username,
            'password': password,
            'enabled': True,
            'added': datetime.now().isoformat()
        }
        
        self.proxies.append(proxy_entry)
        self.save_proxies()
        return True
    
    def remove_proxy(self, index: int) -> bool:
        """Remove proxy by index"""
        if 0 <= index < len(self.proxies):
            self.proxies.pop(index)
            self.save_proxies()
            return True
        return False
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next enabled proxy in rotation"""
        if not self.proxies:
            return None
        
        # Find next enabled proxy
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_proxy_idx]
            self.current_proxy_idx = (self.current_proxy_idx + 1) % len(self.proxies)
            
            if proxy.get('enabled', True):
                return proxy
            attempts += 1
        
        return None
    
    def get_requests_proxy(self, proxy_dict: Optional[Dict] = None) -> Optional[Dict]:
        """
        Get proxy in format for requests library
        
        Returns dict like: {'http': 'http://proxy:port', 'https': 'http://proxy:port'}
        or with auth: {'http': 'http://user:pass@proxy:port', ...}
        """
        if proxy_dict is None:
            proxy_dict = self.get_next_proxy()
        
        if not proxy_dict:
            return None
        
        url = proxy_dict.get('url', '').strip()
        if not url:
            return None
        
        username = proxy_dict.get('username', '').strip()
        password = proxy_dict.get('password', '').strip()
        
        # Add auth if provided
        if username and password:
            # Insert credentials into URL
            protocol = url.split('://')[0] if '://' in url else 'http'
            rest = url.split('://', 1)[1] if '://' in url else url
            url = f"{protocol}://{username}:{password}@{rest}"
        
        # Return in requests library format
        return {
            'http': url,
            'https': url
        }
    
    def test_proxy(self, proxy_dict: Optional[Dict] = None, verbose: bool = False) -> bool:
        """Test if a proxy is working"""
        import requests
        
        if proxy_dict is None:
            proxy_dict = self.get_next_proxy()
        
        if not proxy_dict:
            return False
        
        try:
            proxy_requests = self.get_requests_proxy(proxy_dict)
            if not proxy_requests:
                return False
            
            if verbose:
                print(f"[ProxyManager] Testing {proxy_dict.get('url')}...")
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy_requests,
                timeout=5
            )
            
            if response.status_code == 200:
                if verbose:
                    print(f"[ProxyManager] ✓ Proxy working: {response.json()}")
                return True
            else:
                if verbose:
                    print(f"[ProxyManager] ✗ Proxy returned {response.status_code}")
                return False
        except Exception as e:
            if verbose:
                print(f"[ProxyManager] ✗ Proxy failed: {e}")
            return False
    
    def get_all_proxies(self) -> List[Dict]:
        """Get all configured proxies"""
        return self.proxies.copy()
    
    def fetch_from_proxylist(self, count: int = 10, proxy_types: List[str] = None) -> int:
        """
        Fetch fresh proxies from ProxyList (GitHub) and add them
        
        Args:
            count: Number of proxies to fetch
            proxy_types: List of types to fetch (http, https, socks4, socks5)
            
        Returns:
            Number of proxies added
        """
        if not HAS_PROXY_FETCHER:
            print("[ProxyManager] ProxyFetcher not available - cannot fetch from ProxyList")
            return 0
        
        if proxy_types is None:
            proxy_types = ["http", "https", "socks5"]
        
        try:
            fetcher = ProxyFetcher()
            added = 0
            per_type = max(1, count // len(proxy_types))
            
            for ptype in proxy_types:
                proxies = fetcher.fetch_proxies(limit=per_type, source="auto", force_refresh=False)
                for proxy_url in proxies:
                    if self.add_proxy(proxy_url, proxy_type=ptype):
                        added += 1
                    if added >= count:
                        break
                if added >= count:
                    break
            
            print(f"[ProxyManager] ✓ Added {added} proxies from ProxyList")
            return added
            
        except Exception as e:
            print(f"[ProxyManager] Error fetching from ProxyList: {e}")
            return 0
    
    def disable_proxy(self, index: int):
        """Disable a proxy (don't delete, just mark disabled)"""
        if 0 <= index < len(self.proxies):
            self.proxies[index]['enabled'] = False
            self.save_proxies()
    
    def enable_proxy(self, index: int):
        """Re-enable a disabled proxy"""
        if 0 <= index < len(self.proxies):
            self.proxies[index]['enabled'] = True
            self.save_proxies()
    
    def mark_proxy_failed(self, proxy_url: str):
        """Mark a proxy as failed (disable it)"""
        for i, proxy in enumerate(self.proxies):
            if proxy.get('url') == proxy_url:
                self.proxies[i]['enabled'] = False
                self.proxies[i]['last_failure'] = datetime.now().isoformat()
                self.save_proxies()
                return True
        return False


# Common free proxy sources (for reference - these are public, quality varies)
FREE_PROXY_SOURCES = """
# Free proxy lists (quality varies, use with caution):
# https://www.proxy-list.download/
# https://www.freeproxylists.net/
# https://www.us-proxy.org/
# https://free-proxy-list.com/

# Paid proxy services (more reliable):
# - Bright Data (formerly Luminati)
# - Oxylabs
# - Smartproxy
# - Residential proxies from various providers
# - VPS with rotating IPs

# To add proxies to the app:
# 1. Get proxy URLs (http://ip:port or socks5://ip:port)
# 2. Click "Add Proxy" in the GUI
# 3. Configure username/password if needed
# 4. Test the proxy
# 5. Use in scraper
"""
