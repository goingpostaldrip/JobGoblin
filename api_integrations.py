"""
API Integration Module for Job Scraper APIs
Supports RapidAPI job scrapers: LinkedIn, Indeed, Glassdoor, and aggregators
"""
import os
import time
import hashlib
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = "Mozilla/5.0 (compatible; JobScraperUltimate/2.0)"


class JobAPIBase:
    """Base class for all job API integrations"""
    
    def __init__(self, api_key: Optional[str] = None, rapidapi_key: Optional[str] = None):
        self.api_key = api_key
        self.rapidapi_key = rapidapi_key or os.getenv("RAPIDAPI_KEY")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
    
    def _hash(self, title: str, url: str) -> str:
        """Generate unique hash for job posting"""
        return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()
    
    def _format_result(self, engine: str, query: str, title: str, url: str, snippet: str = "") -> Dict:
        """Format API response into standard job result format"""
        return {
            "engine": engine,
            "query": query,
            "title": title,
            "url": url,
            "snippet": snippet,
            "ts": int(time.time()),
            "hash": self._hash(title, url)
        }


class LinkedInJobAPI(JobAPIBase):
    """LinkedIn Job Search API via RapidAPI"""
    
    API_HOST = "linkedin-job-search-api.p.rapidapi.com"
    API_URL = f"https://{API_HOST}/search"
    
    def __init__(self, api_key: Optional[str] = None):
        rapidapi_key = api_key or os.getenv("LINKEDIN_API_KEY") or os.getenv("RAPIDAPI_KEY")
        super().__init__(api_key=api_key, rapidapi_key=rapidapi_key)
    
    def search(self, keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[Dict]:
        """
        Search LinkedIn jobs using RapidAPI
        
        Args:
            keyword: Job search keywords
            location: Location filter (e.g., "New York, NY")
            max_results: Maximum number of results
            verbose: Print debug info
        
        Returns:
            List of job dictionaries
        """
        if not self.rapidapi_key:
            if verbose:
                print("[LinkedInJobAPI] No API key found. Set RAPIDAPI_KEY or LINKEDIN_API_KEY in .env")
            return []
        
        try:
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.API_HOST
            }
            
            params = {
                "keywords": keyword,
                "location": location,
                "datePosted": "anyTime",
                "sort": "mostRelevant"
            }
            
            if verbose:
                print(f"[LinkedInJobAPI] Searching: {keyword} in {location}")
            
            response = self.session.get(self.API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Parse API response (format varies by specific API)
            jobs = data.get("data", []) or data.get("jobs", []) or data
            
            for job in jobs[:max_results]:
                if isinstance(job, dict):
                    title = job.get("title") or job.get("jobTitle") or job.get("name", "")
                    url = job.get("url") or job.get("jobUrl") or job.get("link", "")
                    company = job.get("company") or job.get("companyName", "")
                    description = job.get("description") or job.get("snippet", "")
                    
                    if title and url:
                        snippet = f"{company}: {description[:200]}" if company else description[:200]
                        results.append(self._format_result(
                            engine="linkedin_api",
                            query=f"{keyword} {location}".strip(),
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
            
            if verbose:
                print(f"[LinkedInJobAPI] Found {len(results)} results")
            
            return results
            
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"[LinkedInJobAPI] Request error: {e}")
            return []
        except Exception as e:
            if verbose:
                print(f"[LinkedInJobAPI] Error: {e}")
            return []


class IndeedJobAPI(JobAPIBase):
    """Indeed Jobs Scraper API via RapidAPI"""
    
    API_HOST = "indeed-jobs-api.p.rapidapi.com"
    API_URL = f"https://{API_HOST}/search"
    
    def __init__(self, api_key: Optional[str] = None):
        rapidapi_key = api_key or os.getenv("INDEED_API_KEY") or os.getenv("RAPIDAPI_KEY")
        super().__init__(api_key=api_key, rapidapi_key=rapidapi_key)
    
    def search(self, keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[Dict]:
        """Search Indeed jobs using RapidAPI"""
        if not self.rapidapi_key:
            if verbose:
                print("[IndeedJobAPI] No API key found. Set RAPIDAPI_KEY or INDEED_API_KEY in .env")
            return []
        
        try:
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.API_HOST
            }
            
            params = {
                "query": keyword,
                "location": location,
                "page": "1"
            }
            
            if verbose:
                print(f"[IndeedJobAPI] Searching: {keyword} in {location}")
            
            response = self.session.get(self.API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            jobs = data.get("jobs", []) or data.get("data", []) or data
            
            for job in jobs[:max_results]:
                if isinstance(job, dict):
                    title = job.get("title") or job.get("jobTitle", "")
                    url = job.get("url") or job.get("jobUrl") or job.get("link", "")
                    company = job.get("company") or job.get("companyName", "")
                    snippet = job.get("description") or job.get("snippet", "")
                    
                    if title and url:
                        full_snippet = f"{company}: {snippet[:200]}" if company else snippet[:200]
                        results.append(self._format_result(
                            engine="indeed_api",
                            query=f"{keyword} {location}".strip(),
                            title=title,
                            url=url,
                            snippet=full_snippet
                        ))
            
            if verbose:
                print(f"[IndeedJobAPI] Found {len(results)} results")
            
            return results
            
        except Exception as e:
            if verbose:
                print(f"[IndeedJobAPI] Error: {e}")
            return []


class GlassdoorJobAPI(JobAPIBase):
    """Glassdoor Job + Reviews API via RapidAPI"""
    
    API_HOST = "glassdoor-job-scraper.p.rapidapi.com"
    API_URL = f"https://{API_HOST}/search"
    
    def __init__(self, api_key: Optional[str] = None):
        rapidapi_key = api_key or os.getenv("GLASSDOOR_API_KEY") or os.getenv("RAPIDAPI_KEY")
        super().__init__(api_key=api_key, rapidapi_key=rapidapi_key)
    
    def search(self, keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[Dict]:
        """Search Glassdoor jobs using RapidAPI"""
        if not self.rapidapi_key:
            if verbose:
                print("[GlassdoorJobAPI] No API key found. Set RAPIDAPI_KEY or GLASSDOOR_API_KEY in .env")
            return []
        
        try:
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.API_HOST
            }
            
            params = {
                "keyword": keyword,
                "location": location
            }
            
            if verbose:
                print(f"[GlassdoorJobAPI] Searching: {keyword} in {location}")
            
            response = self.session.get(self.API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            jobs = data.get("jobs", []) or data.get("data", []) or data
            
            for job in jobs[:max_results]:
                if isinstance(job, dict):
                    title = job.get("jobTitle") or job.get("title", "")
                    url = job.get("jobUrl") or job.get("url") or job.get("link", "")
                    company = job.get("employer") or job.get("company", "")
                    rating = job.get("rating", "")
                    salary = job.get("salary", "")
                    
                    snippet_parts = []
                    if company:
                        snippet_parts.append(company)
                    if rating:
                        snippet_parts.append(f"Rating: {rating}⭐")
                    if salary:
                        snippet_parts.append(f"Salary: {salary}")
                    
                    snippet = " | ".join(snippet_parts)
                    
                    if title and url:
                        results.append(self._format_result(
                            engine="glassdoor_api",
                            query=f"{keyword} {location}".strip(),
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
            
            if verbose:
                print(f"[GlassdoorJobAPI] Found {len(results)} results")
            
            return results
            
        except Exception as e:
            if verbose:
                print(f"[GlassdoorJobAPI] Error: {e}")
            return []


class JobAggregatorAPI(JobAPIBase):
    """Multi-platform Job Aggregator API (LinkedIn + Indeed + Glassdoor + more)"""
    
    API_HOST = "job-search-api1.p.rapidapi.com"
    API_URL = f"https://{API_HOST}/search"
    
    def __init__(self, api_key: Optional[str] = None):
        rapidapi_key = api_key or os.getenv("JOB_AGGREGATOR_API_KEY") or os.getenv("RAPIDAPI_KEY")
        super().__init__(api_key=api_key, rapidapi_key=rapidapi_key)
    
    def search(self, keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[Dict]:
        """Search across multiple job platforms using aggregator API"""
        if not self.rapidapi_key:
            if verbose:
                print("[JobAggregatorAPI] No API key found. Set RAPIDAPI_KEY or JOB_AGGREGATOR_API_KEY in .env")
            return []
        
        try:
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.API_HOST
            }
            
            params = {
                "query": keyword,
                "location": location,
                "page": "1"
            }
            
            if verbose:
                print(f"[JobAggregatorAPI] Searching multi-platform: {keyword} in {location}")
            
            response = self.session.get(self.API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            jobs = data.get("data", []) or data.get("jobs", []) or data
            
            for job in jobs[:max_results]:
                if isinstance(job, dict):
                    title = job.get("title") or job.get("job_title", "")
                    url = job.get("url") or job.get("job_url", "")
                    company = job.get("company_name") or job.get("company", "")
                    source = job.get("source", "aggregator")
                    
                    snippet = f"[{source}] {company}" if company else f"[{source}]"
                    
                    if title and url:
                        results.append(self._format_result(
                            engine="job_aggregator_api",
                            query=f"{keyword} {location}".strip(),
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
            
            if verbose:
                print(f"[JobAggregatorAPI] Found {len(results)} results from multiple platforms")
            
            return results
            
        except Exception as e:
            if verbose:
                print(f"[JobAggregatorAPI] Error: {e}")
            return []


class RemoteJobsAPI(JobAPIBase):
    """Remote Jobs API (RemoteOK, WeWorkRemotely, Remotive aggregated)"""
    
    API_HOST = "remote-jobs-api.p.rapidapi.com"
    API_URL = f"https://{API_HOST}/jobs"
    
    def __init__(self, api_key: Optional[str] = None):
        rapidapi_key = api_key or os.getenv("REMOTE_JOBS_API_KEY") or os.getenv("RAPIDAPI_KEY")
        super().__init__(api_key=api_key, rapidapi_key=rapidapi_key)
    
    def search(self, keyword: str, location: str = "", max_results: int = 20, verbose: bool = False) -> List[Dict]:
        """Search remote jobs across multiple remote job boards"""
        if not self.rapidapi_key:
            if verbose:
                print("[RemoteJobsAPI] No API key found. Set RAPIDAPI_KEY or REMOTE_JOBS_API_KEY in .env")
            return []
        
        try:
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.API_HOST
            }
            
            params = {
                "search": keyword,
                "limit": str(max_results)
            }
            
            if verbose:
                print(f"[RemoteJobsAPI] Searching remote jobs: {keyword}")
            
            response = self.session.get(self.API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            jobs = data if isinstance(data, list) else data.get("jobs", [])
            
            for job in jobs[:max_results]:
                if isinstance(job, dict):
                    title = job.get("position") or job.get("title", "")
                    url = job.get("url") or job.get("apply_url", "")
                    company = job.get("company", "")
                    tags = job.get("tags", [])
                    
                    snippet = f"{company} | Remote"
                    if tags:
                        snippet += f" | {', '.join(tags[:3])}"
                    
                    if title and url:
                        results.append(self._format_result(
                            engine="remote_jobs_api",
                            query=keyword,
                            title=title,
                            url=url,
                            snippet=snippet
                        ))
            
            if verbose:
                print(f"[RemoteJobsAPI] Found {len(results)} remote jobs")
            
            return results
            
        except Exception as e:
            if verbose:
                print(f"[RemoteJobsAPI] Error: {e}")
            return []


# Factory function to get all available API engines
def get_api_engines(verbose: bool = False) -> Dict[str, JobAPIBase]:
    """
    Get all configured API engines
    Returns dict of {engine_name: api_instance}
    """
    engines = {}
    
    # Check which APIs have keys configured
    if os.getenv("RAPIDAPI_KEY") or os.getenv("LINKEDIN_API_KEY"):
        engines["linkedin_api"] = LinkedInJobAPI()
        if verbose:
            print("[API] ✓ LinkedIn API enabled")
    
    if os.getenv("RAPIDAPI_KEY") or os.getenv("INDEED_API_KEY"):
        engines["indeed_api"] = IndeedJobAPI()
        if verbose:
            print("[API] ✓ Indeed API enabled")
    
    if os.getenv("RAPIDAPI_KEY") or os.getenv("GLASSDOOR_API_KEY"):
        engines["glassdoor_api"] = GlassdoorJobAPI()
        if verbose:
            print("[API] ✓ Glassdoor API enabled")
    
    if os.getenv("RAPIDAPI_KEY") or os.getenv("JOB_AGGREGATOR_API_KEY"):
        engines["job_aggregator_api"] = JobAggregatorAPI()
        if verbose:
            print("[API] ✓ Job Aggregator API enabled")
    
    if os.getenv("RAPIDAPI_KEY") or os.getenv("REMOTE_JOBS_API_KEY"):
        engines["remote_jobs_api"] = RemoteJobsAPI()
        if verbose:
            print("[API] ✓ Remote Jobs API enabled")
    
    if not engines and verbose:
        print("[API] ⚠ No API keys configured. Set RAPIDAPI_KEY in .env to enable API features")
    
    return engines


# Test function
if __name__ == "__main__":
    import sys
    
    print("Testing Job API Integrations\n")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    # Test configuration
    test_keyword = sys.argv[1] if len(sys.argv) > 1 else "python developer"
    test_location = sys.argv[2] if len(sys.argv) > 2 else "Remote"
    
    print(f"\nSearch: '{test_keyword}' in '{test_location}'")
    print("=" * 60 + "\n")
    
    engines = get_api_engines(verbose=True)
    
    if not engines:
        print("\n❌ No API engines available!")
        print("Please set RAPIDAPI_KEY in your .env file")
        print("\nGet your key at: https://rapidapi.com")
        sys.exit(1)
    
    print(f"\n✓ Found {len(engines)} API engine(s)\n")
    
    # Test each engine
    for name, api in engines.items():
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print('='*60)
        
        results = api.search(test_keyword, test_location, max_results=5, verbose=True)
        
        if results:
            print(f"\n✓ Results ({len(results)}):")
            for i, job in enumerate(results, 1):
                print(f"\n{i}. {job['title']}")
                print(f"   URL: {job['url']}")
                print(f"   Info: {job['snippet'][:100]}")
        else:
            print("\n⚠ No results found")
        
        time.sleep(1)  # Rate limiting
    
    print("\n" + "="*60)
    print("✓ API Integration Test Complete")
    print("="*60)
