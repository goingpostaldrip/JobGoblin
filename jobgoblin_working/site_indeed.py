# Modular job scraper for Indeed
# Self-healing logic included

def indeed_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://www.indeed.com/jobs?q={keyword}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('a', attrs={'data-hide-spinner': 'true'})
            for card in job_cards[:limit]:
                title = card.get('aria-label', 'Unknown')
                job_url = 'https://www.indeed.com' + card.get('href', '')
                jobs.append({"title": title, "company": "Indeed", "location": location, "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"Indeed error: {e}, retrying...")
            time.sleep(2)
    return jobs
