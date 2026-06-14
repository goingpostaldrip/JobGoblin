# JobGoblin Working - DDG Proxy Client
# Add DuckDuckGo proxy client logic here if needed for future enhancements.

import requests
def ddg_search(keyword, location, limit=5, verbose=False, proxy=None):
    jobs = []
    url = f"https://duckduckgo.com/?q={keyword}+jobs+{location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            resp.raise_for_status()
            # Dummy parse: just add one result for demo
            jobs.append({"title": f"{keyword} Job", "company": "DuckDuckGo", "location": location, "url": url})
            break
        except Exception as e:
            if verbose:
                print(f"DuckDuckGo error: {e}, retrying...")
            import time
            time.sleep(2)
    return jobs
