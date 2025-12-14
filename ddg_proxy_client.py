"""
DuckDuckGo Proxy Client - Use the background proxy server for searches
"""

import requests
from typing import List, Dict

PROXY_SERVER_URL = "http://localhost:8765"

def search_via_proxy(query: str, max_results: int = 10, timeout: int = 30) -> List[Dict[str, str]]:
    """
    Search DuckDuckGo via local proxy server
    
    Args:
        query: Search query
        max_results: Maximum results to return
        timeout: Request timeout in seconds
        
    Returns:
        List of dicts with 'title' and 'url' keys
        
    Raises:
        requests.RequestException: If proxy server is unavailable
    """
    try:
        response = requests.get(
            f"{PROXY_SERVER_URL}/search",
            params={"q": query, "max_results": max_results},
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        raise Exception(f"Proxy server error: {e}")

def is_proxy_available() -> bool:
    """Check if the proxy server is available"""
    try:
        response = requests.get(f"{PROXY_SERVER_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# Example usage
if __name__ == "__main__":
    if is_proxy_available():
        print("✓ Proxy server is available")
        results = search_via_proxy("Python developer", max_results=5)
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   {result['url']}\n")
    else:
        print("✗ Proxy server is not available")
