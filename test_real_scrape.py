#!/usr/bin/env python3
"""
Test a real scrape to verify emails are being found
"""
from search_engines import duckduckgo_search
from email_extractor import extract_emails_from_url

print("=" * 80)
print("TESTING EMAIL EXTRACTION WITH REAL SCRAPE")
print("=" * 80)

# Do a small DuckDuckGo search
print("\n[1] Searching for jobs with DuckDuckGo...")
results = duckduckgo_search("python developer remote jobs", max_results=3, verbose=False)

print(f"Found {len(results)} job listings\n")

# Extract emails from each result
for i, result in enumerate(results, 1):
    print(f"\n[Result {i}] {result.get('title', 'N/A')[:60]}")
    url = result.get('url', '')
    print(f"URL: {url[:70]}")
    
    if url:
        emails, error = extract_emails_from_url(url, timeout=8, verbose=False)
        print(f"Emails found: {len(emails)}")
        if emails:
            for email in list(emails)[:3]:
                print(f"  ✓ {email}")
        if error:
            print(f"Error: {error}")
    else:
        print("No URL available")
    print("-" * 80)

print("\nTest complete!")
