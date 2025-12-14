#!/usr/bin/env python3
"""
Quick email extraction test - just test the email extractor on real URLs
"""
from email_extractor import extract_emails_from_url
import time

print("Testing email extraction from job listing URLs...")
print("=" * 80)

# Test URLs from actual job sites
test_cases = [
    ("DuckDuckGo job snippet", "https://www.indeed.com"),
    ("LinkedIn job page", "https://www.linkedin.com"),
    ("Greenhouse careers", "https://jobs.lever.co"),
]

for name, url in test_cases:
    print(f"\n[{name}]")
    print(f"URL: {url}")
    
    start = time.time()
    emails, error = extract_emails_from_url(url, timeout=10, verbose=True)
    elapsed = time.time() - start
    
    print(f"Status: {error if error else 'OK'}")
    print(f"Emails found: {len(emails)}")
    if emails:
        print(f"  - {', '.join(list(emails)[:5])}")
    print(f"Time: {elapsed:.2f}s")
    print("-" * 80)

print("\nDone!")
