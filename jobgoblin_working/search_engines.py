# JobGoblin Working - Search Engines Utility
# Add search engine logic here if needed for future enhancements.

SEARCH_ENGINES = [
    "Google",
    "Bing",
    "DuckDuckGo"
]

def startpage_search(keyword, location, limit=5, verbose=False, proxy=None):
    jobs = []
    url = f"https://www.startpage.com/search?q={keyword}+jobs+{location}"
    jobs.append({"title": f"{keyword} Job", "company": "Startpage", "location": location, "url": url})
    return jobs

def serpapi_search(keyword, location, limit=5, verbose=False, proxy=None):
    jobs = []
    url = f"https://serpapi.com/search?q={keyword}+jobs+{location}"
    jobs.append({"title": f"{keyword} Job", "company": "SerpAPI", "location": location, "url": url})
    return jobs

def google_cse_search(keyword, location, limit=5, verbose=False, proxy=None):
    jobs = []
    url = f"https://www.google.com/search?q={keyword}+jobs+{location}"
    jobs.append({"title": f"{keyword} Job", "company": "Google CSE", "location": location, "url": url})
    return jobs

def bing_search(keyword, location, limit=5, verbose=False, proxy=None):
    jobs = []
    url = f"https://www.bing.com/search?q={keyword}+jobs+{location}"
    jobs.append({"title": f"{keyword} Job", "company": "Bing", "location": location, "url": url})
    return jobs
