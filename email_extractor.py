"""
Email extraction module - scrapes websites for contact emails
"""
import re
import requests
from typing import List, Set, Dict, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; JobScraperUltimate/1.0)"

# Email regex pattern
EMAIL_REGEX = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    re.IGNORECASE
)

# Patterns to exclude common noreply, notification, and bot emails
EXCLUDE_PATTERNS = [
    r'noreply', r'no-reply', r'no_reply', r'donotreply', r'do-not-reply',
    r'notification', r'notification-email', r'alert', r'automated',
    r'mailer-daemon', r'postmaster', r'support+', r'info+', r'test@',
    r'example\.com', r'localhost', r'invalid', r'fake', r'spam',
    r'sentry', r'@sentry\.', r'jobtoday\.tools'
]

# File extensions that shouldn't be in emails
INVALID_EMAIL_PATTERNS = [
    r'\.png', r'\.jpg', r'\.jpeg', r'\.gif', r'\.svg', r'\.webp', r'\.ico',
    r'\.pdf', r'\.doc', r'\.docx', r'\.xls', r'\.xlsx',
    r'\.zip', r'\.rar', r'\.tar', r'\.gz',
    r'\.mp4', r'\.mp3', r'\.avi', r'\.mov',
    r'\.css', r'\.js', r'\.json', r'\.xml',
    r'\d{3,}x\d{3,}',  # Image dimensions like 1000x500
    r'@2x', r'@3x',  # Retina image markers
    r'-\d{3,}x\d{3,}',  # More image dimension patterns
]

def is_valid_email(email: str) -> bool:
    """Check if email passes validation rules"""
    if not email or not EMAIL_REGEX.match(email):
        return False
    
    email_lower = email.lower()
    
    # Filter out file extensions and image patterns
    for pattern in INVALID_EMAIL_PATTERNS:
        if re.search(pattern, email_lower, re.IGNORECASE):
            return False
    
    # Filter out common exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, email_lower, re.IGNORECASE):
            return False
    
    # Must have at least one letter before @ (not just numbers)
    local_part = email.split('@')[0]
    if not re.search(r'[A-Za-z]', local_part):
        return False
    
    # Domain should have at least one letter (not just numbers/dashes)
    domain_part = email.split('@')[1] if '@' in email else ''
    if not re.search(r'[A-Za-z]', domain_part):
        return False
    
    return True

def extract_emails_from_html(html_content: str, base_url: str = "") -> Set[str]:
    """Extract valid emails from HTML content"""
    emails = set()
    
    # Find all email-like strings in the HTML
    found = EMAIL_REGEX.findall(html_content)
    
    for email in found:
        if is_valid_email(email):
            emails.add(email.lower())
    
    return emails

def extract_emails_from_url(url: str, timeout: int = 10, verbose: bool = False) -> Tuple[Set[str], str]:
    """
    Fetch a URL and extract emails from its content.
    Returns (set of emails, error_message or empty string)
    """
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return set(), "Invalid URL"
    
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        
        if verbose:
            print(f"[email_extractor] Fetched {url} - {len(resp.text)} bytes")
        
        emails = extract_emails_from_html(resp.text, url)
        return emails, ""
        
    except requests.exceptions.Timeout:
        return set(), "Timeout"
    except requests.exceptions.ConnectionError:
        return set(), "Connection error"
    except requests.exceptions.HTTPError as e:
        return set(), f"HTTP {e.response.status_code}"
    except Exception as e:
        if verbose:
            print(f"[email_extractor] Error fetching {url}: {e}")
        return set(), str(type(e).__name__)

def extract_company_emails_from_domain(domain: str, timeout: int = 10, verbose: bool = False) -> Tuple[Set[str], str]:
    """
    Given a domain (e.g., 'example.com'), try to fetch it and extract emails.
    """
    if not domain:
        return set(), "No domain"
    
    # Construct full URL if just domain is provided
    if not domain.startswith('http'):
        url = f"https://{domain}"
    else:
        url = domain
    
    return extract_emails_from_url(url, timeout, verbose)

def extract_from_job_results(job_records: List[Dict], verbose: bool = False) -> Dict[str, Set[str]]:
    """
    Given a list of job result records, extract emails from company URLs.
    Returns dict mapping company domain/name -> set of emails
    """
    company_emails = {}
    
    for record in job_records:
        url = record.get('url', '')
        if not url:
            continue
        
        # Extract domain from URL
        try:
            domain = urlparse(url).netloc
        except:
            continue
        
        if domain not in company_emails:
            if verbose:
                print(f"[email_extractor] Extracting emails from {url}")
            
            emails, error = extract_emails_from_url(url, verbose=verbose)
            company_emails[domain] = {
                'url': url,
                'emails': emails,
                'error': error,
                'title': record.get('title', ''),
                'job_url': url
            }
    
    return company_emails

def filter_and_dedupe_emails(company_emails: Dict) -> Dict[str, Dict]:
    """
    Filter duplicates and organize emails by domain.
    Returns dict with unique emails mapped to job sources.
    """
    all_emails = {}
    
    for domain, info in company_emails.items():
        for email in info.get('emails', set()):
            if email not in all_emails:
                all_emails[email] = {
                    'email': email,
                    'domains': set(),
                    'sources': [],
                    'job_titles': set()
                }
            
            all_emails[email]['domains'].add(domain)
            if info.get('job_url'):
                all_emails[email]['sources'].append(info['job_url'])
            if info.get('title'):
                all_emails[email]['job_titles'].add(info['title'])
    
    return all_emails
