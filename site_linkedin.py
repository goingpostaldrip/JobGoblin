import time
import hashlib
from typing import List, Dict
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class LinkedInResult(Dict):
    pass

def _hash(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8", errors="ignore")).hexdigest()

def _create_driver(headless: bool = True):
    """Create a Selenium WebDriver for LinkedIn scraping."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"[linkedin] Failed to create WebDriver: {e}")
        return None

def linkedin_login(driver, email: str, password: str, verbose: bool = False) -> bool:
    """Log into LinkedIn account."""
    try:
        if verbose:
            print("[linkedin] Navigating to login page...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        
        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(email)
        
        # Enter password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click login button
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()
        
        # Wait for page to load
        time.sleep(4)
        
        # Check if login was successful
        if "feed" in driver.current_url or "mynetwork" in driver.current_url:
            if verbose:
                print("[linkedin] Login successful!")
            return True
        else:
            if verbose:
                print("[linkedin] Login may have failed - unexpected URL")
            return False
            
    except Exception as e:
        if verbose:
            print(f"[linkedin] Login error: {e}")
        return False

def linkedin_job_search(keyword: str, location: str = "", email: str = "", password: str = "", 
                       max_results: int = 20, verbose: bool = False) -> List[LinkedInResult]:
    """
    Scrape LinkedIn job search results.
    
    Args:
        keyword: Job title or keyword to search
        location: Optional location filter
        email: LinkedIn account email (optional - can also use logged-in browser)
        password: LinkedIn account password (optional)
        max_results: Maximum number of results to return
        verbose: Print debug messages
    
    Returns:
        List of job results with title, url, company, location, snippet, engine, hash
    """
    driver = _create_driver(headless=True)
    if not driver:
        return []
    
    try:
        # If credentials provided, log in
        if email and password:
            if not linkedin_login(driver, email, password, verbose):
                if verbose:
                    print("[linkedin] Proceeding without authentication...")
        
        # Build search URL
        search_query = keyword
        if location:
            search_query = f"{keyword} in {location}"
        
        # Use LinkedIn jobs search page
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}"
        if location:
            url += f"&location={location}"
        
        if verbose:
            print(f"[linkedin] GET {url}")
        
        driver.get(url)
        time.sleep(3)
        
        # Scroll to load more results
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 3000);")
            time.sleep(1)
        
        results: List[LinkedInResult] = []
        seen_urls = set()
        
        # Try to extract job listings
        job_cards = driver.find_elements(By.XPATH, "//div[@class='base-card' or @class='job-card-container']")
        
        if verbose:
            print(f"[linkedin] Found {len(job_cards)} job cards")
        
        for card in job_cards[:max_results]:
            try:
                # Extract job title
                title_elem = card.find_element(By.XPATH, ".//h3[@class='base-search-card__title']")
                title = title_elem.text.strip()
                
                # Extract company
                company_elem = card.find_element(By.XPATH, ".//h4[@class='base-search-card__subtitle']")
                company = company_elem.text.strip()
                
                # Extract location
                location_elem = card.find_element(By.XPATH, ".//span[@class='job-search-card__location']")
                result_location = location_elem.text.strip()
                
                # Extract URL by clicking the card
                link_elem = card.find_element(By.XPATH, ".//a[@class='base-card__full-link']")
                job_url = link_elem.get_attribute("href")
                
                # Extract snippet if available
                try:
                    snippet_elem = card.find_element(By.XPATH, ".//p[@class='base-search-card__snippet']")
                    snippet = snippet_elem.text.strip()
                except:
                    snippet = ""
                
                # Avoid duplicates
                if job_url in seen_urls:
                    continue
                seen_urls.add(job_url)
                
                # Clean up the URL (remove parameters if needed)
                if "?" in job_url:
                    job_url = job_url.split("?")[0]
                
                result = LinkedInResult({
                    "title": title,
                    "company": company,
                    "location": result_location,
                    "url": job_url,
                    "snippet": snippet or f"Position at {company} in {result_location}",
                    "engine": "linkedin",
                    "hash": _hash(title, job_url)
                })
                
                results.append(result)
                
                if verbose:
                    print(f"[linkedin] Found: {title} @ {company}")
                
            except Exception as e:
                if verbose:
                    print(f"[linkedin] Error parsing job card: {e}")
                continue
        
        if verbose:
            print(f"[linkedin] Total results: {len(results)}")
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"[linkedin] Error: {e}")
        return []
    
    finally:
        driver.quit()

def linkedin_search_via_api(keyword: str, location: str = "", max_results: int = 20, 
                           verbose: bool = False) -> List[LinkedInResult]:
    """
    Alternative: Search LinkedIn jobs via API without authentication.
    Uses public job board data when available.
    """
    try:
        # LinkedIn job search API endpoint
        headers = {"User-Agent": USER_AGENT}
        
        search_query = keyword
        if location:
            search_query = f"{keyword} in {location}"
        
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting"
        params = {
            "keywords": keyword,
            "location": location or "",
            "start": 0,
            "count": min(max_results, 25)
        }
        
        if verbose:
            print(f"[linkedin_api] GET {url}")
        
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        
        results: List[LinkedInResult] = []
        
        # Parse response (format depends on LinkedIn's current structure)
        # LinkedIn has changed their API frequently, so this may need updates
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"[linkedin_api] Error: {e}")
        return []
