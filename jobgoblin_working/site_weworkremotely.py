# Modular job scraper for WeWorkRemotely
# Self-healing logic included

def weworkremotely_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('section', class_='jobs')
            for section in job_cards:
                for card in section.find_all('li', class_='feature')[:limit]:
                    title = card.find('span', class_='title').text.strip() if card.find('span', class_='title') else 'Unknown'
                    job_url = 'https://weworkremotely.com' + card.find('a').get('href', '') if card.find('a') else url
                    jobs.append({"title": title, "company": "WeWorkRemotely", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"WeWorkRemotely error: {e}, retrying...")
            time.sleep(2)
    return jobs
