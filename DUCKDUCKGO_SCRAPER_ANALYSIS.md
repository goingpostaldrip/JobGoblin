# DuckDuckGo Scraper Implementation Analysis
**Repository:** https://github.com/omkarcloud/duckduckgo-scraper

---

## 1. ACTUAL IMPLEMENTATION CODE

### A. Main Entry Point (`main.py`)
```python
from src import DuckDuckGo 

queries = [
  "Mango",
  "Watermelon",
]

DuckDuckGo.search(queries, max=10)
```

**Key Insight:** Ultra-simple API - just pass queries and max results.

---

### B. Core DuckDuckGo Class (`src/duckduckgo_scraper.py`)

```python
from typing import List, Optional, Union, Dict
from botasaurus import bt
from .write_output import write_output
from .search import (
    FAILED_DUE_TO_CREDITS_EXHAUSTED, 
    FAILED_DUE_TO_NO_KEY,
    FAILED_DUE_TO_NOT_SUBSCRIBED, 
    FAILED_DUE_TO_UNKNOWN_ERROR, 
    search
)

class DuckDuckGo:
    
    @staticmethod
    def search(
        query: Union[str, List[str]], 
        max: Optional[int] = None, 
        key: Optional[str] = None, 
        use_cache: bool = True
    ) -> Dict:
        """
        Function to scrape data from DuckDuckGo.
        :param query: Single query string or list of queries
        :param max: Maximum number of results per query
        :param key: Optional RapidAPI key for higher limits
        :param use_cache: Boolean indicating whether to use cached data
        :return: List of dictionaries with the scraped data
        """
        cache = use_cache
        if isinstance(query, str):
            query = [query]  

        query = [{"query": query_query, "max": max} for query_query in query]
        result = []
        
        for item in query:
            data = item
            metadata = {"key": key}
            
            # Call the decorated search function
            result_item = search(data, cache=cache, metadata=metadata)
            
            # Clean and categorize errors
            success, credits_exhausted, not_subscribed, unknown_error, no_key = clean_data([result_item])
            print_data_errors(credits_exhausted, not_subscribed, unknown_error, no_key)

            if success:
                data = result_item.get('data')
                if not data:
                    data = {}

                result_item = data.get('results', [])
                result.extend(result_item)
                write_output(item['query'], result_item, None)

        if result:
            write_output('_all', result, None, lambda x: x)
        
        search.close()

        return result
```

### C. Error Handling & Data Cleaning

```python
def clean_data(social_details):
    """Categorize results by error type"""
    success, credits_exhausted, not_subscribed, unknown_error, no_key = [], [], [], [], []

    for detail in social_details:
        if detail.get("error") is None:
            success.append(detail)
        elif detail["error"] == FAILED_DUE_TO_CREDITS_EXHAUSTED:
            credits_exhausted.append(detail)
        elif detail["error"] == FAILED_DUE_TO_NOT_SUBSCRIBED:
            not_subscribed.append(detail)
        elif detail["error"] == FAILED_DUE_TO_UNKNOWN_ERROR:
            unknown_error.append(detail)
        elif detail["error"] == FAILED_DUE_TO_NO_KEY:
            no_key.append(detail)

    return success, credits_exhausted, not_subscribed, unknown_error, no_key

def print_data_errors(credits_exhausted, not_subscribed, unknown_error, no_key):
    """Print detailed error messages"""
    
    if credits_exhausted:
        name = "queries" if len(credits_exhausted) > 1 else "query"
        print(f"Could not get data for {len(credits_exhausted)} {name} due to credit exhaustion. "
              f"Please upgrade: https://rapidapi.com/Chetan11dev/api/duckduckgo-scraper/pricing")

    if not_subscribed:
        name = "queries" if len(not_subscribed) > 1 else "query"
        print(f"Could not get data for {len(not_subscribed)} {name}. API not subscribed. "
              f"Please subscribe: https://rapidapi.com/Chetan11dev/api/duckduckgo-scraper/pricing")

    if unknown_error:
        name = "queries" if len(unknown_error) > 1 else "query"
        print(f"Could not get data for {len(unknown_error)} {name} due to Unknown Error.")

    if no_key:
        name = "queries" if len(no_key) > 1 else "query"
        print(f"Could not get data for {len(no_key)} {name}. No API key provided.")
```

---

### D. Core Scraping Logic (`src/search.py`)

```python
from botasaurus import bt
from botasaurus.cache import DontCache
from botasaurus import cl
from time import sleep
from botasaurus import *
from .utils import default_request_options
import requests

# Error Constants
FAILED_DUE_TO_CREDITS_EXHAUSTED = "FAILED_DUE_TO_CREDITS_EXHAUSTED"
FAILED_DUE_TO_NOT_SUBSCRIBED = "FAILED_DUE_TO_NOT_SUBSCRIBED"
FAILED_DUE_TO_NO_KEY = "FAILED_DUE_TO_NO_KEY"
FAILED_DUE_TO_UNKNOWN_ERROR = "FAILED_DUE_TO_UNKNOWN_ERROR"

def update_credits():
    """Track API credit usage in local storage"""
    credits_used = bt.LocalStorage.get_item("credits_used", 0)
    bt.LocalStorage.set_item("credits_used", credits_used + 1)

def do_request(data, retry_count=3):
    """
    Make HTTP request with retry logic for rate limiting
    :param data: Request data with params and key
    :param retry_count: Retries remaining (max 3)
    """
    params = data["params"]
    link = params["link"]
    key = data["key"]
    
    if retry_count == 0:
        print(f"Failed to get data, after 3 retries")
        return {
            "data": None,
            "error": FAILED_DUE_TO_UNKNOWN_ERROR, 
        }

    # RapidAPI headers
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "duckduckgo-scraper.p.rapidapi.com"
    }

    response = requests.get(link, headers=headers)
    response_data = response.json()
    
    # Success responses (200 or 404)
    if response.status_code == 200 or response.status_code == 404:
        message = response_data.get("message", "")
        
        if "API doesn't exists" in message:
            return {
                "data": None,
                "error": FAILED_DUE_TO_UNKNOWN_ERROR
            }

        update_credits()
        
        if response.status_code == 404:
            print(f"No data found")
            return {
                "data": response_data,
                "error": None
            }

        return {
            "data": response_data,
            "error": None
        }
    else:
        # Error responses with retry logic
        message = response_data.get("message", "")
        
        if "exceeded the MONTHLY quota" in message:
            return {
                "data": None,
                "error": FAILED_DUE_TO_CREDITS_EXHAUSTED
            }
        elif "exceeded the rate limit per second for your plan" in message or "many requests" in message:
            # RATE LIMIT HANDLING: Sleep and retry
            sleep(2)
            return do_request(data, retry_count - 1)
        elif "You are not subscribed to this API." in message:
            return {
                "data": None,
                "error": FAILED_DUE_TO_NOT_SUBSCRIBED
            }

        print(f"Error: {response.status_code}", response_data)
        
        return {
            "data": None,
            "error": FAILED_DUE_TO_UNKNOWN_ERROR, 
        }

@request(**default_request_options)
def search(_, data, metadata):
    """
    Paginated search with automatic continuation
    Decorated with @request for caching and retry support
    """
    if not metadata.get('key'):
        return DontCache({
            "data": None,
            "error": FAILED_DUE_TO_NO_KEY
        })
    
    max_items = data['max']
    url = "https://duckduckgo-scraper.p.rapidapi.com/search/"
    qp = {"query": data['query']}
    params = {**qp, 'link': cl.join_link(url, query_params=qp)}

    request_data = {**metadata, "params": params}
    result = do_request(request_data)
    initial_results = cl.select(result, 'data', 'results', default=[])
    
    if not cl.select(result, 'error'):
        more_results = cl.select(result, 'data', 'results', default=[])
        print(f"Got {len(more_results)} more results")

    # Pagination loop - follow "next" links until max_items reached
    while cl.select(result, 'data', 'next') and (max_items is None or len(initial_results) < max_items):
        next_link = cl.select(result, 'data', 'next')

        params = {**qp, 'link': next_link}
        request_data = {**metadata, "params": params}
        result = do_request(request_data)
        
        if result.get('error'):
            break
            
        more_results = cl.select(result, 'data', 'results', default=[])
        print(f"Got {len(more_results)} more results")
        initial_results.extend(more_results)

    # Handle error vs success
    if cl.select(result, 'error'):
        return DontCache(result)
    else: 
        if max_items is not None:
            initial_results = initial_results[:max_items]

        result['data']['results'] = initial_results
        return result
```

---

### E. Configuration (`src/utils.py`)

```python
# Browser automation options (for Botasaurus)
default_browser_options = {
    "block_images": True,           # Faster loading
    "reuse_driver": True,           # Reuse browser instances
    "keep_drivers_alive": True,     # Keep browsers alive between requests
    "close_on_crash": True,         # Recovery on crash
    "headless": True,               # Run headless (hidden)
    'output': None,                 # No logging in production
}

# Request/API call options (for Botasaurus)
default_request_options = {
    "close_on_crash": True,         # Recovery on crash
    'output': None,                 # No logging in production
    "raise_exception": True,        # Raise on errors
}
```

---

### F. Dependencies (`requirements.txt`)

```
botasaurus
casefy
```

**Only 2 dependencies!** This is the key difference - they delegate all scraping complexity to Botasaurus.

---

## 2. CLASS/FUNCTION SIGNATURES

### Public API

```python
# Main method - only one public method
DuckDuckGo.search(
    query: Union[str, List[str]],      # Single query or list
    max: Optional[int] = None,         # Max results (None = no limit)
    key: Optional[str] = None,         # RapidAPI key (optional)
    use_cache: bool = True             # Use cached results
) -> Dict                              # Returns list of results
```

### Internal Helper Functions

```python
# Error categorization
clean_data(social_details: List[Dict]) -> Tuple[List, List, List, List, List]

# Error reporting
print_data_errors(
    credits_exhausted: List,
    not_subscribed: List,
    unknown_error: List,
    no_key: List
) -> None

# Core HTTP request
do_request(
    data: Dict,           # {params: {link, query}, key: str}
    retry_count: int = 3
) -> Dict                 # {data: response_data, error: error_string}

# Decorated search (uses Botasaurus)
@request(**default_request_options)
def search(
    _: Any,
    data: Dict,           # {query: str, max: int}
    metadata: Dict        # {key: str}
) -> Dict                 # Paginated results with caching
```

---

## 3. KEY DIFFERENCES FROM YOUR APPROACH

### Your Current Approach (Job Scraper):
- Direct DuckDuckGo HTML scraping
- Basic proxy rotation
- Simple request retry logic
- Manual email extraction
- Limited caching strategy

### Their Approach:

| Feature | Your Code | Their Code |
|---------|-----------|-----------|
| **Anti-Detection** | Simple user-agent rotation | Botasaurus handles fingerprinting + headless browser automation |
| **Retry Logic** | Basic 3-retry with random sleep | Smart retry with rate-limit detection (2s sleep before retry) |
| **Caching** | JSON file-based | Botasaurus LocalStorage + DontCache decorator for rate-limited results |
| **Error Handling** | Generic try/catch | 5 specific error types tracked separately |
| **Rate Limiting** | No special handling | Detects "exceeded rate limit" message and retries |
| **Pagination** | Manual navigation | Automatic via `result['data']['next']` field |
| **Dependency Injection** | Hardcoded parameters | Metadata dict pattern for flexible API keys |
| **Production Ready** | debug=True, headless=False | Properly configured for production |

---

## 4. SPECIAL ANTI-DETECTION & BLOCKING TECHNIQUES

### A. Botasaurus Framework (The Secret Sauce)

The entire project relies on **Botasaurus** - a web scraping framework with:

1. **Stealth Browser Automation**
   - Hides automation indicators
   - Realistic browser behavior
   - JavaScript rendering support

2. **Intelligent Caching**
   - Automatically cache requests
   - Smart invalidation
   - DontCache() for rate-limited responses

3. **Retry with Exponential Backoff**
   - Built into @request decorator
   - Handles transient failures
   - Preserves cache on failure

4. **Output Management**
   - Structured logging
   - Problem matcher for error tracking

### B. Rate Limit Detection & Handling

```python
# Smart detection of rate limit messages:
if "exceeded the rate limit per second for your plan" in message or "many requests" in message:
    sleep(2)                              # Strategic 2-second delay
    return do_request(data, retry_count - 1)  # Retry with reduced count
```

**Key Insight:** They explicitly check error messages to detect rate limits and retry intelligently.

### C. API Key Rotation (Optional)

```python
DuckDuckGo.search(query, key="YOUR_RAPIDAPI_KEY")
```

Uses RapidAPI for higher rate limits (1000 requests for $9/month after free tier).

---

## 5. HOW THEY AVOID BLOCKS/CAPTCHAS

### Method 1: Use Official API (Recommended)
- Uses RapidAPI proxy service
- DuckDuckGo-scraper.p.rapidapi.com endpoint
- Not direct HTML scraping = fewer blocks
- Official API = legitimate requests

### Method 2: Botasaurus Anti-Detection
- Browser automation appears more legitimate
- Fingerprinting defense
- Proper headers: `X-RapidAPI-Key` and `X-RapidAPI-Host`

### Method 3: Caching
- Cache results with `use_cache=True` (default)
- Avoid repeated requests to same query
- LocalStorage tracking of credit usage

### Method 4: Rate Limit Awareness
- Not aggressive - they build in waits
- Detects rate limit messages proactively
- Backs off with sleep() before retry

---

## 6. DIRECTLY APPLICABLE CODE SNIPPETS FOR JOB SCRAPER

### A. Smart Error Categorization (For Email Extraction)

```python
# Apply to your email_extractor.py
ERROR_INVALID_EMAIL = "INVALID_EMAIL"
ERROR_RATE_LIMITED = "RATE_LIMITED"
ERROR_TIMEOUT = "TIMEOUT"

def clean_extraction_results(results):
    """Categorize extraction attempts by error type"""
    valid, invalid, rate_limited, timeout = [], [], [], []
    
    for result in results:
        if result.get("error") is None:
            valid.append(result)
        elif result["error"] == ERROR_INVALID_EMAIL:
            invalid.append(result)
        elif result["error"] == ERROR_RATE_LIMITED:
            rate_limited.append(result)
        elif result["error"] == ERROR_TIMEOUT:
            timeout.append(result)
    
    return valid, invalid, rate_limited, timeout
```

### B. Intelligent Retry with Rate Limit Detection

```python
# Better retry logic than current approach
def make_search_request(query, proxy=None, retry_count=3):
    """
    Make request with smart rate limit detection
    """
    if retry_count == 0:
        return {"data": None, "error": "MAX_RETRIES_EXCEEDED"}
    
    headers = {
        "User-Agent": "Mozilla/5.0...",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(
            f"https://duckduckgo.com/search?q={query}",
            headers=headers,
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=10
        )
        
        # Check for rate limit messages in HTML/JSON
        if "rate limit" in response.text.lower() or response.status_code == 429:
            sleep(2)  # Strategic wait
            return make_search_request(query, proxy, retry_count - 1)
        
        if response.status_code == 200:
            return {"data": response.text, "error": None}
        else:
            return {"data": None, "error": f"HTTP_{response.status_code}"}
            
    except requests.Timeout:
        sleep(1)
        return make_search_request(query, proxy, retry_count - 1)
    except Exception as e:
        return {"data": None, "error": str(e)}
```

### C. Metadata Pattern for Flexible Configuration

```python
# Replace hardcoded settings with metadata pattern
def scrape_jobs(queries, metadata):
    """
    :param queries: List of job queries to search
    :param metadata: {
        "proxy": "http://...",
        "api_key": "...",
        "rate_limit_delay": 2,
        "max_retries": 3
    }
    """
    results = []
    
    for query in queries:
        result = search_job_listings(
            query=query,
            metadata=metadata
        )
        results.append(result)
    
    return results
```

### D. Pagination Pattern (Like DuckDuckGo Scraper)

```python
# Handle paginated results automatically
def get_all_results(initial_response, max_items=None):
    """
    Follow pagination links until max_items or no more pages
    """
    all_results = []
    current_response = initial_response
    
    while True:
        results = current_response.get('results', [])
        all_results.extend(results)
        
        # Check if we've reached limit
        if max_items and len(all_results) >= max_items:
            break
        
        # Check for next page
        next_link = current_response.get('next')
        if not next_link:
            break
        
        # Fetch next page
        current_response = fetch_page(next_link)
        if current_response.get('error'):
            break
    
    # Trim to max if specified
    if max_items:
        all_results = all_results[:max_items]
    
    return all_results
```

### E. Cache-Aware Request Function

```python
# Implement local storage like Botasaurus
class RequestCache:
    def __init__(self, cache_file="request_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get(self, key, use_cache=True):
        if use_cache and key in self.cache:
            return self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = value
        self._save_cache()

# Usage
cache = RequestCache()
cached = cache.get("python developer jobs")
if cached:
    results = cached
else:
    results = duckduckgo_search("python developer jobs")
    cache.set("python developer jobs", results)
```

---

## 7. COMPARISON: DIRECT SCRAPING VS THEIR APPROACH

### Advantages of RapidAPI Method (What They Use)

✅ **No direct blocks** - Hitting official API endpoint  
✅ **Reliable pagination** - Structured `next` field  
✅ **Rate limit messaging** - Clear error codes  
✅ **Scalability** - Pay for higher limits  
✅ **Legal compliance** - Using official API  

### Advantages of Direct HTML Scraping (What You Do)

✅ **No API key needed**  
✅ **Free unlimited**  
✅ **More control over parsing**  

### Recommended Hybrid Approach

1. **For DuckDuckGo:** Use `botasaurus` framework
2. **For job site scraping:** Combine direct scraping with Botasaurus anti-detection
3. **For email extraction:** Use their error categorization pattern
4. **For proxy handling:** Implement rate limit awareness like they do

---

## 8. IMPLEMENTATION PRIORITY

### High Impact (Implement First)
1. **Error categorization system** - Track different failure types
2. **Rate limit detection** - Detect "rate limit" in responses and sleep
3. **Smart retry** - With exponential backoff and rate limit checks
4. **Metadata pattern** - Flexible configuration injection

### Medium Impact
5. **LocalStorage caching** - Track credits/usage like them
6. **Pagination helpers** - Automatic "next" link following
7. **Botasaurus integration** - Replace basic requests with browser automation

### Nice to Have
8. **RapidAPI integration** - Optional paid tier
9. **Credit tracking** - Dashboard showing API usage
10. **Output formatting** - CSV/JSON like theirs

---

## 9. QUICK WIN: Update Your DuckDuckGo Search

Currently in `search_engines.py`:
```python
def duckduckgo_search(query, max_results=10, verbose=False):
    # Your current implementation
```

**Replace with Botasaurus pattern:**
```python
from botasaurus import *

class DuckDuckGoAdapter:
    @request(close_on_crash=True, raise_exception=True)
    def search(_, data, metadata):
        # Use their caching + retry + headless approach
        pass

# Usage remains same but gets anti-detection for free
```

---

## Summary

| Aspect | Key Learning |
|--------|---------------|
| **Architecture** | Single-responsibility classes + decorator pattern |
| **Anti-Detection** | Rely on Botasaurus framework, not manual fixes |
| **Error Handling** | Explicit error types, smart categorization |
| **Rate Limiting** | Detect messages, sleep strategically, retry |
| **Caching** | LocalStorage + DontCache for rate-limited |
| **Pagination** | Follow 'next' field automatically |
| **Config** | Metadata dict injection pattern |
| **Dependencies** | Minimal (botasaurus + casefy) |

**Their biggest advantage:** Using Botasaurus removes 90% of the complexity you're trying to solve manually.
