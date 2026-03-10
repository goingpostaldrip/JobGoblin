"""
DuckDuckGo Proxy Server - Background HTTP proxy for DDG searches
Runs as a subprocess, provides local endpoint at http://localhost:8765/search
"""

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import sys

app = Flask(__name__)

# Disable Flask logging to keep it invisible
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

current_ua_index = 0

def get_user_agent():
    """Rotate user agents"""
    global current_ua_index
    ua = USER_AGENTS[current_ua_index]
    current_ua_index = (current_ua_index + 1) % len(USER_AGENTS)
    return ua

@app.route('/search', methods=['GET'])
def search():
    """
    DuckDuckGo search endpoint
    Query params:
        q: search query
        max_results: maximum results (default 10)
    """
    query = request.args.get('q', '')
    max_results = int(request.args.get('max_results', 10))
    
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    
    try:
        results = duckduckgo_search(query, max_results)
        return jsonify({
            "query": query,
            "count": len(results),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "ddg-proxy"})

def duckduckgo_search(query: str, max_results: int = 10):
    """
    Perform DuckDuckGo HTML search
    
    Args:
        query: Search query string
        max_results: Maximum number of results
        
    Returns:
        List of dicts with 'title' and 'url'
    """
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": get_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    params = {"q": query}
    
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    
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
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in parsed:
                    actual_url = parsed["uddg"][0]
                    results.append({
                        "title": title,
                        "url": actual_url
                    })
            except:
                continue
    
    return results

if __name__ == '__main__':
    import os
    # Run on localhost:8765, suppress output
    print("DDG_PROXY_READY", flush=True)  # Signal readiness
    sys.stdout = open(os.devnull, 'w')  # Suppress further output
    sys.stderr = open(os.devnull, 'w')
    app.run(host='127.0.0.1', port=8765, debug=False, use_reloader=False)
