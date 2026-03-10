# Modular job scraper for Remotive
# Self-healing logic included

def remotive_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://remotive.com/remote-jobs/search?search={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('div', class_='job-list-item')
            for card in job_cards[:limit]:
                title = card.find('h2').text.strip() if card.find('h2') else 'Unknown'
                job_url = card.find('a').get('href', '') if card.find('a') else url
                jobs.append({"title": title, "company": "Remotive", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"Remotive error: {e}, retrying...")
            time.sleep(2)
    return jobs
