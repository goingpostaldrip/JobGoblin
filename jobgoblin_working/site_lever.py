# Modular job scraper for Lever
# Self-healing logic included

def lever_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://jobs.lever.co/search/?keywords={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('a', class_='posting-title')
            for card in job_cards[:limit]:
                title = card.text.strip()
                job_url = card.get('href', '')
                jobs.append({"title": title, "company": "Lever", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"Lever error: {e}, retrying...")
            time.sleep(2)
    return jobs
