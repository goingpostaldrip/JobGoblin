"""
Automatic proxy discovery - finds free proxies from public sources
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import time
import random

class ProxyFinder:
    """Automatically discovers and validates free proxies"""
    
    # Fallback public proxies (rotate these periodically)
    FALLBACK_PROXIES = [
        "http://proxy.emule-security.net:8080",
        "http://103.145.128.83:8080",
        "http://45.79.91.208:8080",
        "http://185.107.47.171:8080",
        "http://189.41.85.189:8080",
    ]
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.found_proxies: List[Dict] = []
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    
    def find_from_freeproxylists(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Scrape proxies from freeproxylists.net
        Returns list of proxy URLs
        """
        proxies = []
        try:
            url = "https://www.freeproxylists.net/"
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching freeproxylists.net...")
            
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find proxy table rows
            table = soup.find('table', class_='table')
            if not table:
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows[:limit]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    
                    if ip and port and self._is_valid_ip(ip):
                        proxy_url = f"http://{ip}:{port}"
                        proxies.append(proxy_url)
                        if verbose:
                            print(f"  Found: {proxy_url}")
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with freeproxylists: {e}")
            return []
    
    def find_from_github_speedx(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from TheSpeedX/PROXY-List GitHub repository
        This is one of the most reliable free proxy lists available
        """
        proxies = []
        try:
            # GitHub raw content URLs for different proxy types
            urls = [
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (TheSpeedX/PROXY-List)...")
            
            for url in urls:
                try:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    resp.raise_for_status()
                    
                    # Each line is a proxy in format: IP:PORT
                    for line in resp.text.strip().split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            # Parse IP:PORT format
                            parts = line.split(':')
                            if len(parts) == 2:
                                ip, port = parts
                                if self._is_valid_ip(ip):
                                    # Determine proxy type from URL
                                    if 'socks5' in url:
                                        proxy_url = f"socks5://{ip}:{port}"
                                    elif 'socks4' in url:
                                        proxy_url = f"socks4://{ip}:{port}"
                                    else:
                                        proxy_url = f"http://{ip}:{port}"
                                    
                                    proxies.append(proxy_url)
                                    if verbose:
                                        print(f"  Found: {proxy_url}")
                                    
                                    if len(proxies) >= limit:
                                        return proxies[:limit]
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error fetching {url.split('/')[-1]}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with GitHub PROXY-List: {e}")
            return []
    
    def find_from_freeproxylists(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Scrape proxies from proxy-list.download
        """
        proxies = []
        try:
            url = "https://www.proxy-list.download/api/v1/get?type=http"
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching proxy-list.download...")
            
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            data = resp.json()
            
            if 'LISTA' in data:
                for proxy in data['LISTA'][:limit]:
                    ip = proxy.get('IP')
                    port = proxy.get('PORT')
                    
                    if ip and port and self._is_valid_ip(ip):
                        proxy_url = f"http://{ip}:{port}"
                        proxies.append(proxy_url)
                        if verbose:
                            print(f"  Found: {proxy_url}")
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with proxy-list.download: {e}")
            return []
    
    def find_from_us_proxy(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Scrape proxies from us-proxy.org
        """
        proxies = []
        try:
            url = "https://www.us-proxy.org/"
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching us-proxy.org...")
            
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find proxy table
            table = soup.find('table', class_='table')
            if not table:
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows[:limit]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    
                    if ip and port and self._is_valid_ip(ip):
                        proxy_url = f"http://{ip}:{port}"
                        proxies.append(proxy_url)
                        if verbose:
                            print(f"  Found: {proxy_url}")
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with us-proxy.org: {e}")
            return []
    
    def find_from_free_proxy_list(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Scrape proxies from free-proxy-list.com
        """
        proxies = []
        try:
            url = "https://free-proxy-list.com/"
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching free-proxy-list.com...")
            
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find proxy table
            table = soup.find('table', class_='table')
            if not table:
                return []
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows[:limit]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    
                    if ip and port and self._is_valid_ip(ip):
                        proxy_url = f"http://{ip}:{port}"
                        proxies.append(proxy_url)
                        if verbose:
                            print(f"  Found: {proxy_url}")
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with free-proxy-list: {e}")
            return []
    
    def find_from_proxifly(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from Proxifly GitHub repository
        Updated every 5 minutes with validated proxies
        """
        proxies = []
        try:
            urls = [
                "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
                "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt",
                "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt",
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (Proxifly)...")
            
            for url in urls:
                try:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    resp.raise_for_status()
                    
                    for line in resp.text.strip().split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                ip, port = parts
                                if self._is_valid_ip(ip):
                                    if 'socks5' in url:
                                        proxy_url = f"socks5://{ip}:{port}"
                                    elif 'socks4' in url:
                                        proxy_url = f"socks4://{ip}:{port}"
                                    else:
                                        proxy_url = f"http://{ip}:{port}"
                                    
                                    proxies.append(proxy_url)
                                    if verbose:
                                        print(f"  Found: {proxy_url}")
                                    
                                    if len(proxies) >= limit:
                                        return proxies[:limit]
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error fetching {url.split('/')[-2]}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with Proxifly: {e}")
            return []
    
    def find_from_zebbern(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from Zebbern/Proxy-Scraper GitHub repository
        Updated hourly
        """
        proxies = []
        try:
            urls = [
                "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/main/http.txt",
                "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/main/https.txt",
                "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/main/socks4.txt",
                "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/main/socks5.txt",
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (Zebbern/Proxy-Scraper)...")
            
            for url in urls:
                try:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    resp.raise_for_status()
                    
                    for line in resp.text.strip().split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                ip, port = parts
                                if self._is_valid_ip(ip):
                                    if 'socks5' in url:
                                        proxy_url = f"socks5://{ip}:{port}"
                                    elif 'socks4' in url:
                                        proxy_url = f"socks4://{ip}:{port}"
                                    else:
                                        proxy_url = f"http://{ip}:{port}"
                                    
                                    proxies.append(proxy_url)
                                    if verbose:
                                        print(f"  Found: {proxy_url}")
                                    
                                    if len(proxies) >= limit:
                                        return proxies[:limit]
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error fetching {url.split('/')[-1]}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with Zebbern: {e}")
            return []
    
    def find_from_proxylist_haitham(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from haithamaouati/ProxyList GitHub repository
        Updated hourly with verified proxies
        """
        proxies = []
        try:
            # This repo hosts a web page, need to fetch the actual proxy files
            # Based on the web page structure, proxies are linked from index.html
            urls = [
                "https://raw.githubusercontent.com/haithamaouati/ProxyList/main/socks4.txt",
                "https://raw.githubusercontent.com/haithamaouati/ProxyList/main/socks5.txt",
                "https://raw.githubusercontent.com/haithamaouati/ProxyList/main/http.txt",
                "https://raw.githubusercontent.com/haithamaouati/ProxyList/main/https.txt",
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (ProxyList by Haitham)...")
            
            for url in urls:
                try:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    if resp.status_code == 404:
                        continue  # File might not exist
                    resp.raise_for_status()
                    
                    for line in resp.text.strip().split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                ip, port = parts
                                if self._is_valid_ip(ip):
                                    if 'socks5' in url:
                                        proxy_url = f"socks5://{ip}:{port}"
                                    elif 'socks4' in url:
                                        proxy_url = f"socks4://{ip}:{port}"
                                    else:
                                        proxy_url = f"http://{ip}:{port}"
                                    
                                    proxies.append(proxy_url)
                                    if verbose:
                                        print(f"  Found: {proxy_url}")
                                    
                                    if len(proxies) >= limit:
                                        return proxies[:limit]
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error fetching {url.split('/')[-1]}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with ProxyList: {e}")
            return []
    
    def find_from_ninjah(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from haithamaouati/Ninjah GitHub repository
        Uses same proxy list as ProxyList (by same author)
        """
        # Ninjah is just a bash script that downloads from the same sources
        # We'll use the ProxyList method which has the actual proxy files
        return self.find_from_proxylist_haitham(limit=limit, verbose=verbose)
    
    def find_from_monosans(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from monosans/proxy-list GitHub repository
        Updated hourly with geolocation info
        """
        proxies = []
        try:
            urls = [
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
                "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (monosans/proxy-list)...")
            
            for url in urls:
                try:
                    resp = requests.get(url, headers=headers, timeout=self.timeout)
                    resp.raise_for_status()
                    
                    for line in resp.text.strip().split('\n'):
                        line = line.strip()
                        if line and ':' in line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                ip, port = parts
                                if self._is_valid_ip(ip):
                                    if 'socks5' in url:
                                        proxy_url = f"socks5://{ip}:{port}"
                                    elif 'socks4' in url:
                                        proxy_url = f"socks4://{ip}:{port}"
                                    else:
                                        proxy_url = f"http://{ip}:{port}"
                                    
                                    proxies.append(proxy_url)
                                    if verbose:
                                        print(f"  Found: {proxy_url}")
                                    
                                    if len(proxies) >= limit:
                                        return proxies[:limit]
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error fetching {url.split('/')[-1]}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with monosans: {e}")
            return []
    
    def find_from_clarketm(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from clarketm/proxy-list GitHub repository
        Updated daily, simple raw list
        """
        proxies = []
        try:
            url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching GitHub (clarketm/proxy-list)...")
            
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            for line in resp.text.strip().split('\n'):
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        ip, port = parts
                        if self._is_valid_ip(ip):
                            proxy_url = f"http://{ip}:{port}"
                            proxies.append(proxy_url)
                            if verbose:
                                print(f"  Found: {proxy_url}")
                            
                            if len(proxies) >= limit:
                                return proxies[:limit]
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with clarketm: {e}")
            return []
    
    def find_from_proxypool_api(self, limit: int = 10, verbose: bool = False) -> List[str]:
        """
        Fetch proxies from public ProxyPool API endpoints
        Based on Python3WebSpider/ProxyPool project
        """
        proxies = []
        try:
            # Try common public ProxyPool API endpoints
            api_urls = [
                "http://proxypool.scrape.center/random",  # Get random proxy
                "http://demo.spiderpy.cn/get/",  # Public demo endpoint
            ]
            
            headers = {"User-Agent": self.user_agent}
            
            if verbose:
                print("[ProxyFinder] Searching ProxyPool APIs...")
            
            for api_url in api_urls:
                try:
                    # Try to get multiple proxies
                    for _ in range(min(limit, 5)):
                        resp = requests.get(api_url, headers=headers, timeout=self.timeout)
                        if resp.status_code == 200:
                            proxy = resp.text.strip()
                            if proxy and ':' in proxy:
                                # Check if it's just IP:PORT or full URL
                                if not proxy.startswith('http'):
                                    proxy = f"http://{proxy}"
                                proxies.append(proxy)
                                if verbose:
                                    print(f"  Found: {proxy}")
                                
                                if len(proxies) >= limit:
                                    return proxies[:limit]
                        time.sleep(0.2)  # Small delay between requests
                except Exception as e:
                    if verbose:
                        print(f"[ProxyFinder] Error with {api_url}: {e}")
                    continue
            
            return proxies[:limit]
            
        except Exception as e:
            if verbose:
                print(f"[ProxyFinder] Error with ProxyPool API: {e}")
            return []
    
    def find_all_sources(self, limit_per_source: int = 5, verbose: bool = False) -> List[str]:
        """
        Search all available sources and return combined list
        """
        all_proxies = []
        
        sources = [
            (self.find_from_github_speedx, "GitHub (TheSpeedX/PROXY-List)"),
            (self.find_from_proxifly, "GitHub (Proxifly)"),
            (self.find_from_monosans, "GitHub (monosans/proxy-list)"),
            (self.find_from_clarketm, "GitHub (clarketm/proxy-list)"),
            (self.find_from_zebbern, "GitHub (Zebbern/Proxy-Scraper)"),
            (self.find_from_proxylist_haitham, "GitHub (ProxyList)"),
            (self.find_from_proxypool_api, "ProxyPool API"),
            (self.find_from_free_proxy_list, "free-proxy-list.com"),
            (self.find_from_us_proxy, "us-proxy.org"),
        ]
        
        for finder_func, source_name in sources:
            if verbose:
                print(f"\n[ProxyFinder] Trying {source_name}...")
            
            try:
                proxies = finder_func(limit=limit_per_source, verbose=verbose)
                all_proxies.extend(proxies)
                time.sleep(0.5)  # Be respectful to servers
            except Exception as e:
                if verbose:
                    print(f"[ProxyFinder] Failed to get proxies from {source_name}: {e}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for proxy in all_proxies:
            if proxy not in seen:
                seen.add(proxy)
                unique.append(proxy)
        
        if verbose:
            print(f"\n[ProxyFinder] Found {len(unique)} unique proxies total")
        
        return unique
    
    def test_proxy(self, proxy_url: str, verbose: bool = False) -> bool:
        """
        Test if a proxy works
        """
        try:
            proxies = {'http': proxy_url, 'https': proxy_url}
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=5
            )
            working = response.status_code == 200
            if verbose:
                status = "✓ WORKING" if working else "✗ FAILED"
                print(f"  {proxy_url}: {status}")
            return working
        except Exception as e:
            if verbose:
                print(f"  {proxy_url}: ✗ FAILED ({type(e).__name__})")
            return False
    
    def find_and_validate(self, limit: int = 20, verbose: bool = False) -> List[str]:
        """
        Find proxies and test them, returning only working ones
        Falls back to fallback proxies if discovery fails
        """
        if verbose:
            print(f"[ProxyFinder] Searching for {limit} working proxies...")
        
        all_found = self.find_all_sources(limit_per_source=limit, verbose=verbose)
        
        # Add fallback proxies as last resort
        if not all_found:
            if verbose:
                print(f"[ProxyFinder] No proxies discovered, trying fallback list...")
            # Shuffle and use fallback proxies
            fallback = self.FALLBACK_PROXIES.copy()
            random.shuffle(fallback)
            all_found.extend(fallback)
        
        if verbose:
            print(f"\n[ProxyFinder] Testing {len(all_found)} proxies...")
        
        working = []
        for proxy in all_found:
            if self.test_proxy(proxy, verbose=verbose):
                working.append(proxy)
                if len(working) >= limit:
                    break
        
        if verbose:
            print(f"\n[ProxyFinder] ✓ Found {len(working)} working proxies")
        
        return working
    
    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Check if string is a valid IP address"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except:
            return False


if __name__ == "__main__":
    # Test the proxy finder
    finder = ProxyFinder()
    print("Finding working proxies...\n")
    
    proxies = finder.find_and_validate(limit=5, verbose=True)
    
    print("\n" + "="*60)
    print("WORKING PROXIES:")
    for proxy in proxies:
        print(f"  {proxy}")
