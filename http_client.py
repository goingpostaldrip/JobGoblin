"""
Centralized HTTP client with automatic proxy support
All scrapers should use this instead of direct requests.get()
"""

import requests
from typing import Optional, Dict, Any
from proxy_manager import ProxyManager

# Global proxy manager instance
_proxy_manager = None

def get_proxy_manager():
    """Get or create the global proxy manager"""
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def get_with_proxy(
    url: str,
    use_proxy: bool = True,
    retry_without_proxy: bool = True,
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    verbose: bool = False,
    **kwargs
) -> requests.Response:
    """
    Make HTTP GET request with automatic proxy support
    
    Args:
        url: URL to fetch
        use_proxy: Whether to try using a proxy
        retry_without_proxy: If proxy fails, retry without proxy
        timeout: Request timeout in seconds
        headers: Optional HTTP headers
        params: Optional query parameters
        verbose: Print debug information
        **kwargs: Additional arguments passed to requests.get()
    
    Returns:
        requests.Response object
        
    Raises:
        requests.RequestException: If request fails
    """
    proxies = None
    used_proxy = False
    
    if use_proxy:
        proxy_mgr = get_proxy_manager()
        if proxy_mgr and proxy_mgr.proxies:
            proxy_dict = proxy_mgr.get_next_proxy()
            if proxy_dict:
                proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                if proxies:
                    used_proxy = True
                    if verbose:
                        print(f"[HTTP] Using proxy: {proxy_dict.get('url')}")
    
    try:
        if verbose:
            print(f"[HTTP] GET {url} (proxy={'enabled' if used_proxy else 'disabled'})")
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            proxies=proxies,
            **kwargs
        )
        
        return response
        
    except Exception as e:
        if verbose:
            print(f"[HTTP] Error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # Retry without proxy if enabled and we were using one
        if used_proxy and retry_without_proxy:
            if verbose:
                print(f"[HTTP] Retrying without proxy...")
            
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=timeout,
                proxies=None,
                **kwargs
            )
            
            return response
        else:
            raise

def post_with_proxy(
    url: str,
    use_proxy: bool = True,
    retry_without_proxy: bool = True,
    timeout: int = 30,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    verbose: bool = False,
    **kwargs
) -> requests.Response:
    """
    Make HTTP POST request with automatic proxy support
    
    Args:
        url: URL to post to
        use_proxy: Whether to try using a proxy
        retry_without_proxy: If proxy fails, retry without proxy
        timeout: Request timeout in seconds
        headers: Optional HTTP headers
        data: Optional form data
        json: Optional JSON data
        verbose: Print debug information
        **kwargs: Additional arguments passed to requests.post()
    
    Returns:
        requests.Response object
        
    Raises:
        requests.RequestException: If request fails
    """
    proxies = None
    used_proxy = False
    
    if use_proxy:
        proxy_mgr = get_proxy_manager()
        if proxy_mgr and proxy_mgr.proxies:
            proxy_dict = proxy_mgr.get_next_proxy()
            if proxy_dict:
                proxies = proxy_mgr.get_requests_proxy(proxy_dict)
                if proxies:
                    used_proxy = True
                    if verbose:
                        print(f"[HTTP] Using proxy: {proxy_dict.get('url')}")
    
    try:
        if verbose:
            print(f"[HTTP] POST {url} (proxy={'enabled' if used_proxy else 'disabled'})")
        
        response = requests.post(
            url,
            headers=headers,
            data=data,
            json=json,
            timeout=timeout,
            proxies=proxies,
            **kwargs
        )
        
        return response
        
    except Exception as e:
        if verbose:
            print(f"[HTTP] Error with {'proxy' if used_proxy else 'direct'}: {e}")
        
        # Retry without proxy if enabled and we were using one
        if used_proxy and retry_without_proxy:
            if verbose:
                print(f"[HTTP] Retrying without proxy...")
            
            response = requests.post(
                url,
                headers=headers,
                data=data,
                json=json,
                timeout=timeout,
                proxies=None,
                **kwargs
            )
            
            return response
        else:
            raise

# Convenience alias
http_get = get_with_proxy
http_post = post_with_proxy
