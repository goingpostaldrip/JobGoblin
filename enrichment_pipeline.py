"""
Enrichment Pipeline - Enrich job listings with emails, company data, and validation.
Integrates with multiple APIs and data sources to enhance job results.
"""

import re
import json
import requests
from typing import List, Dict, Optional
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urljoin, urlparse

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class JobEnrichment:
    """Enrich job results with additional data."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.email_cache = {}  # Cache for extracted emails
        self.company_cache = {}  # Cache for company info
    
    def enrich_job(self, job: Dict) -> Dict:
        """
        Enrich a single job record with emails, company info, and validation.
        
        Args:
            job: Job dictionary with at least 'title', 'url', 'company', 'snippet'
        
        Returns:
            Enriched job dictionary with new fields: emails, company_info, score
        """
        enriched = job.copy()
        
        # Try to extract emails from the job URL and company website
        emails = self._extract_emails_from_job(job)
        enriched["emails"] = emails
        enriched["email_count"] = len(emails)
        
        # Try to get company information
        company_info = self._get_company_info(job.get("company", ""))
        enriched["company_info"] = company_info
        
        # Calculate enrichment score
        enriched["enrichment_score"] = self._calculate_score(enriched)
        
        return enriched
    
    def enrich_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Enrich multiple job records."""
        enriched = []
        for job in jobs:
            try:
                enriched_job = self.enrich_job(job)
                enriched.append(enriched_job)
            except Exception as e:
                if self.verbose:
                    print(f"[enrichment] Error enriching job: {e}")
                enriched.append(job)  # Return original if enrichment fails
        
        return enriched
    
    def _extract_emails_from_job(self, job: Dict) -> List[str]:
        """
        Extract email addresses from job posting and company website.
        
        Args:
            job: Job record with url and company
        
        Returns:
            List of valid email addresses
        """
        emails = set()
        
        # Extract from job URL
        try:
            job_emails = self._extract_emails_from_url(job.get("url", ""))
            emails.update(job_emails)
        except Exception as e:
            if self.verbose:
                print(f"[enrichment] Error extracting from job URL: {e}")
        
        # Try to find company website and extract emails from there
        company = job.get("company", "")
        if company:
            try:
                company_site = self._find_company_website(company)
                if company_site:
                    company_emails = self._extract_emails_from_url(company_site, limit=3)
                    emails.update(company_emails)
            except Exception as e:
                if self.verbose:
                    print(f"[enrichment] Error finding company website: {e}")
        
        # Validate all emails
        validated = []
        for email in emails:
            if self._validate_email(email):
                validated.append(email)
        
        return list(validated)[:5]  # Return top 5 emails
    
    def _extract_emails_from_url(self, url: str, limit: int = 10) -> List[str]:
        """
        Fetch URL and extract email addresses from content.
        
        Args:
            url: URL to scrape
            limit: Maximum number of emails to extract
        
        Returns:
            List of email addresses found
        """
        if not url:
            return []
        
        # Check cache first
        if url in self.email_cache:
            return self.email_cache[url]
        
        try:
            headers = {"User-Agent": USER_AGENT}
            resp = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()
            
            text = resp.text.lower()
            
            # Find email addresses using regex
            email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
            matches = re.findall(email_pattern, text)
            
            # Filter out common non-contact emails
            filtered = []
            exclude_keywords = ['noreply', 'no-reply', 'admin', 'test', 'example', 'sample']
            
            for email in matches:
                if not any(keyword in email.lower() for keyword in exclude_keywords):
                    filtered.append(email)
            
            # Deduplicate and limit
            unique = list(set(filtered))[:limit]
            
            # Cache results
            self.email_cache[url] = unique
            
            return unique
            
        except Exception as e:
            if self.verbose:
                print(f"[enrichment] Error fetching {url}: {e}")
            return []
    
    def _validate_email(self, email: str) -> bool:
        """
        Validate email address format and basic deliverability.
        
        Args:
            email: Email address to validate
        
        Returns:
            True if valid, False otherwise
        """
        try:
            valid = validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _find_company_website(self, company_name: str) -> Optional[str]:
        """
        Find company website using simple heuristics and API.
        
        Args:
            company_name: Name of the company
        
        Returns:
            Company website URL or None
        """
        if not company_name:
            return None
        
        # Check cache
        if company_name in self.company_cache:
            cached = self.company_cache[company_name]
            return cached.get("website")
        
        try:
            # Simple heuristic: try common domain patterns
            company_safe = company_name.lower().replace(" ", "")
            for tld in [".com", ".io", ".co", ".org", ".net"]:
                test_url = f"https://{company_safe}{tld}"
                try:
                    resp = requests.head(test_url, timeout=3)
                    if resp.status_code < 400:
                        self.company_cache[company_name] = {"website": test_url}
                        return test_url
                except:
                    pass
            
            # Try with spaces replaced by hyphens
            company_hyphen = company_name.lower().replace(" ", "-")
            for tld in [".com", ".io", ".co", ".org", ".net"]:
                test_url = f"https://{company_hyphen}{tld}"
                try:
                    resp = requests.head(test_url, timeout=3)
                    if resp.status_code < 400:
                        self.company_cache[company_name] = {"website": test_url}
                        return test_url
                except:
                    pass
            
            return None
            
        except Exception as e:
            if self.verbose:
                print(f"[enrichment] Error finding company website: {e}")
            return None
    
    def _get_company_info(self, company_name: str) -> Dict:
        """
        Get company information from cached sources or APIs.
        
        Args:
            company_name: Name of the company
        
        Returns:
            Dictionary with company info
        """
        if not company_name:
            return {}
        
        # Check cache
        if company_name in self.company_cache:
            return self.company_cache[company_name]
        
        try:
            website = self._find_company_website(company_name)
            
            info = {
                "name": company_name,
                "website": website,
            }
            
            # Cache the result
            self.company_cache[company_name] = info
            
            return info
            
        except Exception as e:
            if self.verbose:
                print(f"[enrichment] Error getting company info: {e}")
            return {"name": company_name}
    
    def _calculate_score(self, enriched_job: Dict) -> float:
        """
        Calculate enrichment quality score.
        
        Factors:
        - Email count (up to 5 emails = 5 points)
        - Company website found (5 points)
        - Valid snippet (2 points)
        
        Returns:
            Score from 0 to 12
        """
        score = 0.0
        
        # Email count score
        email_count = enriched_job.get("email_count", 0)
        score += min(email_count, 5)
        
        # Company website score
        if enriched_job.get("company_info", {}).get("website"):
            score += 5
        
        # Content quality score
        snippet = enriched_job.get("snippet", "")
        if snippet and len(snippet) > 50:
            score += 2
        
        return score


def filter_by_enrichment_score(jobs: List[Dict], min_score: float = 5.0) -> List[Dict]:
    """
    Filter jobs by enrichment score.
    
    Args:
        jobs: List of enriched job records
        min_score: Minimum enrichment score to keep
    
    Returns:
        Filtered list of jobs
    """
    return [j for j in jobs if j.get("enrichment_score", 0) >= min_score]


def sort_by_enrichment(jobs: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sort jobs by enrichment score.
    
    Args:
        jobs: List of enriched job records
        reverse: Sort descending (highest score first) if True
    
    Returns:
        Sorted list of jobs
    """
    return sorted(jobs, key=lambda j: j.get("enrichment_score", 0), reverse=reverse)


def export_enriched_jobs(jobs: List[Dict], filepath: str, format: str = "json") -> bool:
    """
    Export enriched jobs to file.
    
    Args:
        jobs: List of enriched job records
        filepath: Output file path
        format: Output format ('json' or 'csv')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            return True
        
        elif format == "csv":
            import csv
            if not jobs:
                return True
            
            # Get all unique keys
            keys = set()
            for job in jobs:
                keys.update(job.keys())
            
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=sorted(keys))
                writer.writeheader()
                
                for job in jobs:
                    # Convert lists to comma-separated strings
                    row = {}
                    for k, v in job.items():
                        if isinstance(v, list):
                            row[k] = ",".join(str(x) for x in v)
                        elif isinstance(v, dict):
                            row[k] = json.dumps(v)
                        else:
                            row[k] = v
                    writer.writerow(row)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"[enrichment] Error exporting jobs: {e}")
        return False
