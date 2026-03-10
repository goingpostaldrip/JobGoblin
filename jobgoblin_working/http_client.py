# JobGoblin Working - HTTP Client
# Add HTTP client logic here if needed for future enhancements.

import requests

class HttpClient:
    def __init__(self, proxy=None):
        self.proxy = proxy

    def get(self, url, headers=None):
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        try:
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"HTTP error: {e}")
            return None
