"""
JobGoblin - Flask Web Application
Convert the desktop GUI to a web app for online deployment
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import threading
from datetime import datetime
from search_engines import ENGINE_FUNCS
from site_indeed import indeed_search
from site_greenhouse import greenhouse_search
from site_lever import lever_search
from site_simplyhired import simplyhired_search
from normalize import normalize_record, is_relevant
from email_extractor import extract_from_job_results, filter_and_dedupe_emails
from email_manager import EmailManager
from email_sender import EmailSender
import smtplib
import ssl
from email.mime.text import MIMEText
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Global state
scraping_state = {
    'active': False,
    'progress': 0,
    'status': 'Ready',
    'results': [],
    'emails': {}
}


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/engines', methods=['GET'])
def get_engines():
    """Get available search engines"""
    engines = [
        {'name': 'DuckDuckGo', 'key': 'duckduckgo', 'requires_api': False},
        {'name': 'Google CSE', 'key': 'google_cse', 'requires_api': True},
        {'name': 'Bing', 'key': 'bing', 'requires_api': True},
        {'name': 'SerpAPI', 'key': 'serpapi', 'requires_api': True},
        {'name': 'Indeed', 'key': 'indeed', 'requires_api': False},
        {'name': 'Greenhouse', 'key': 'greenhouse', 'requires_api': False},
        {'name': 'Lever', 'key': 'lever', 'requires_api': False},
        {'name': 'SimplyHired', 'key': 'simplyhired', 'requires_api': False},
    ]
    return jsonify(engines)


@app.route('/api/scrape', methods=['POST'])
def start_scrape():
    """Start a scraping job"""
    if scraping_state['active']:
        return jsonify({'error': 'Scraping already in progress'}), 400

    data = request.json
    keywords = [k.strip() for k in data.get('keywords', '').split(',') if k.strip()]
    locations = [l.strip() for l in data.get('locations', '').split(',') if l.strip()]
    engines = data.get('engines', [])
    max_results = int(data.get('max_results', 10))
    extract_emails = data.get('extract_emails', False)

    if not keywords or not engines:
        return jsonify({'error': 'Keywords and engines required'}), 400

    scraping_state['active'] = True
    scraping_state['progress'] = 0
    scraping_state['status'] = 'Starting...'
    scraping_state['results'] = []
    scraping_state['emails'] = {}

    # Run scraping in background
    thread = threading.Thread(
        target=run_scrape_background,
        args=(keywords, locations, engines, max_results, extract_emails),
        daemon=True
    )
    thread.start()

    return jsonify({'status': 'Scraping started'})


def run_scrape_background(keywords, locations, engines, max_results, extract_emails):
    """Background scraping task"""
    try:
        WEB_ENGINES = {"duckduckgo", "google_cse", "bing", "serpapi"}
        SITE_ENGINES = {"indeed", "greenhouse", "lever", "simplyhired"}

        all_results = []
        queries = []

        # Build queries
        for kw in keywords:
            if locations:
                for loc in locations:
                    queries.append(f"{kw} {loc}")
            else:
                queries.append(kw)

        total_steps = len(queries) * len(engines)
        step = 0

        # Run web engines
        for query in queries:
            for engine in engines:
                if not scraping_state['active']:
                    break

                if engine in WEB_ENGINES:
                    try:
                        fn = ENGINE_FUNCS.get(engine)
                        if fn:
                            results = fn(query, max_results=max_results, verbose=False)
                            filtered = [normalize_record(r) for r in results 
                                      if is_relevant(r.get('title', ''), r.get('snippet', ''), keywords, 1.0)]
                            all_results.extend(filtered)
                    except Exception as e:
                        pass

                step += 1
                scraping_state['progress'] = int((step / total_steps) * 100)
                scraping_state['status'] = f"Scraping {engine}: {query}"
                time.sleep(1)

        # Run site engines
        for engine in engines:
            if not scraping_state['active']:
                break

            if engine in SITE_ENGINES:
                for kw in keywords:
                    locs = locations if locations else [""]
                    for loc in locs:
                        try:
                            if engine == "indeed":
                                results = indeed_search(kw, loc, max_results=max_results, verbose=False)
                            elif engine == "greenhouse":
                                results = greenhouse_search(kw, loc, max_results=max_results, verbose=False)
                            elif engine == "lever":
                                results = lever_search(kw, loc, max_results=max_results, verbose=False)
                            elif engine == "simplyhired":
                                results = simplyhired_search(kw, loc, max_results=max_results, verbose=False)
                            else:
                                results = []

                            filtered = [normalize_record(r) for r in results 
                                      if is_relevant(r.get('title', ''), r.get('snippet', ''), keywords, 1.0)]
                            all_results.extend(filtered)
                        except Exception as e:
                            pass

                        step += 1
                        scraping_state['progress'] = int((step / total_steps) * 100)
                        scraping_state['status'] = f"Scraping {engine}: {kw}"
                        time.sleep(1)

        # Deduplicate
        seen = set()
        unique_results = []
        for r in all_results:
            url = r.get('url')
            if url and url not in seen:
                seen.add(url)
                unique_results.append(r)

        scraping_state['results'] = unique_results

        # Extract emails
        if extract_emails:
            scraping_state['status'] = 'Extracting emails...'
            company_emails = extract_from_job_results(unique_results, verbose=False)
            scraping_state['emails'] = filter_and_dedupe_emails(company_emails)

        scraping_state['status'] = f'✅ Complete! Found {len(unique_results)} jobs, {len(scraping_state["emails"])} emails'
        scraping_state['progress'] = 100

    except Exception as e:
        scraping_state['status'] = f'❌ Error: {str(e)}'
    finally:
        scraping_state['active'] = False


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current scraping status"""
    return jsonify({
        'active': scraping_state['active'],
        'progress': scraping_state['progress'],
        'status': scraping_state['status'],
        'jobs_count': len(scraping_state['results']),
        'emails_count': len(scraping_state['emails'])
    })


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get scraped results"""
    return jsonify({
        'jobs': scraping_state['results'][:100],  # Limit to 100
        'emails': list(scraping_state['emails'].keys())[:100]
    })


@app.route('/api/export', methods=['GET'])
def export_results():
    """Export results as JSON"""
    data = {
        'timestamp': datetime.now().isoformat(),
        'jobs': scraping_state['results'],
        'emails': scraping_state['emails']
    }
    
    filename = f"jobgoblin_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return send_file(filename, as_attachment=True)


@app.route('/api/email', methods=['POST'])
def email_results():
    """Email results to user"""
    data = request.json
    recipient = data.get('recipient', '').strip()
    subject = data.get('subject', 'JobGoblin Results').strip()

    if not recipient or '@' not in recipient:
        return jsonify({'error': 'Valid email required'}), 400

    try:
        # Prepare email body
        body = f"""JobGoblin - Scraped Job Results
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Jobs: {len(scraping_state['results'])}
Total Emails: {len(scraping_state['emails'])}

{'='*80}\n\nTop 10 Jobs:\n\n"""

        for idx, job in enumerate(scraping_state['results'][:10], 1):
            body += f"[{idx}] {job.get('title', 'No Title')}\n"
            body += f"URL: {job.get('url', 'N/A')}\n\n"

        # Send via SMTP
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))

        if smtp_user and smtp_pass:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = recipient

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            return jsonify({'status': 'Email sent successfully'})
        else:
            return jsonify({'error': 'Email credentials not configured'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stop', methods=['POST'])
def stop_scrape():
    """Stop scraping"""
    scraping_state['active'] = False
    return jsonify({'status': 'Scraping stopped'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
