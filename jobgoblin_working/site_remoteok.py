# Modular job scraper for RemoteOK
# Self-healing logic included

def remoteok_search(keyword, location, limit=5, verbose=False):
    import requests
    import time
    jobs = []
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    from bs4 import BeautifulSoup
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            job_cards = soup.find_all('tr', class_='job')
            for card in job_cards[:limit]:
                title = card.find('h2').text.strip() if card.find('h2') else 'Unknown'
                job_url = 'https://remoteok.com' + card.get('data-url', '')
                jobs.append({"title": title, "company": "RemoteOK", "location": "Remote", "url": job_url})
            break
        except Exception as e:
            if verbose:
                print(f"RemoteOK error: {e}, retrying...")
            time.sleep(2)
    return jobs
