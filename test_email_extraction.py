#!/usr/bin/env python3
"""
Test script to debug email extraction during a scrape
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Test a simple scrape with verbose email extraction
from cli import main as cli_main
from email_extractor import extract_emails_from_url, extract_from_job_results

print("=" * 80)
print("EMAIL EXTRACTION TEST")
print("=" * 80)

# Test 1: Direct email extraction from a known job site
print("\n[TEST 1] Direct URL email extraction")
print("-" * 80)

test_urls = [
    "https://www.indeed.com/jobs?q=python+developer&l=remote",
    "https://www.linkedin.com/jobs/search/?keywords=python",
    "https://www.greenhouse.io",
]

for test_url in test_urls:
    print(f"\nTesting: {test_url}")
    emails, error = extract_emails_from_url(test_url, verbose=True, timeout=15)
    print(f"Found {len(emails)} emails: {emails}")
    if error:
        print(f"Error: {error}")

# Test 2: Run actual scraper with small job count
print("\n\n[TEST 2] Running scraper with max_results=5")
print("-" * 80)

sys.argv = [
    "cli.py",
    "--keywords", "Python Developer",
    "--location", "Remote",
    "--max_results", "5",
    "--engines", "duckduckgo",
    "--verbose"
]

try:
    # Import and run scraper
    from cli import search_jobs
    results = search_jobs(
        keywords="Python Developer",
        location="Remote",
        engines=["duckduckgo"],
        max_results=5,
        verbose=True
    )
    
    print(f"\n\nGot {len(results)} job results")
    
    # Now extract emails from those results
    print("\n[TEST 3] Extracting emails from job results")
    print("-" * 80)
    
    for i, result in enumerate(results[:3]):  # Test first 3
        print(f"\n[Result {i+1}] {result.get('title', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        
        emails, error = extract_emails_from_url(result.get('url', ''), verbose=True, timeout=15)
        print(f"Found {len(emails)} emails: {emails}")
        if error:
            print(f"Error: {error}")
        print("-" * 40)
    
except Exception as e:
    print(f"Error during scrape test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
