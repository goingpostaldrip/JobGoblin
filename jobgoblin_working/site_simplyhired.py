# Modular job scraper for SimplyHired
# Self-healing logic included

def simplyhired_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://www.simplyhired.com/search?q={keyword}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('a', class_='job-link')
            for card in job_cards[:limit]:
                title = card.text.strip()
                job_url = 'https://www.simplyhired.com' + card.get('href', '')
                jobs.append({"title": title, "company": "SimplyHired", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"SimplyHired error: {e}, retrying...")
            time.sleep(2)
    return jobs
