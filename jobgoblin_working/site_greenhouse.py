# Modular job scraper for Greenhouse
# Self-healing logic included

def greenhouse_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://boards.greenhouse.io/search?query={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('div', class_='opening')
            for card in job_cards[:limit]:
                title = card.find('a').text.strip() if card.find('a') else 'Unknown'
                job_url = card.find('a').get('href', '') if card.find('a') else url
                jobs.append({"title": title, "company": "Greenhouse", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"Greenhouse error: {e}, retrying...")
            time.sleep(2)
    return jobs
