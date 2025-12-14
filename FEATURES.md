# JOB SCRAPER ULTIMATE - Enhanced Edition

Complete job scraping, email extraction, and email campaign automation system.

## New Features

### 1. **Email Extraction from Job Postings**
- Automatically scrapes discovered job posting URLs to extract contact emails
- Validates emails to remove common noreply/bot accounts
- Saves all extracted emails to CSV file: `output/found_emails.csv`
- Deduplicates emails and tracks domains and job titles for each contact

### 2. **Bulk Email Campaign Management**
- **Daily Limit**: Enforces maximum 50 emails per day
- **Tracking**: Tracks which emails were sent each day
- **History**: Maintains complete send history in `output/email_send_history.json`
- **Status**: Logs success/failure for each email sent

### 3. **Multiple Email Backend Support**
- **SendGrid**: Via `SENDGRID_API_KEY` environment variable
- **SMTP**: Via `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` env vars
- Automatic fallback detection - uses SendGrid if available, falls back to SMTP

## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.\.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Method 1: Using the Batch File (Windows)
```batch
run_job_scraper.bat
```

This will prompt you for:
- Keywords to search for (e.g., "Python Developer,Data Scientist")
- Locations (e.g., "New York,Los Angeles")
- Search engines to use
- Whether to extract emails from found job postings
- Whether to send emails to extracted contacts (max 50/day)
- Additional recipient emails for results summary

### Method 2: Command Line

Basic scraping:
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,simplyhired
```

With email extraction:
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,simplyhired --extract-emails
```

With email extraction AND sending (50/day limit):
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,simplyhired --extract-emails --send-emails
```

### CLI Arguments

**Search Arguments:**
- `--keywords` *(required)* - Comma-separated keywords
- `--locations` - Comma-separated locations (optional)
- `--engines` - Search engines: `duckduckgo`, `google_cse`, `bing`, `serpapi`, `indeed`, `greenhouse`, `lever`, `simplyhired`, `linkedin`, `glassdoor`, `ziprecruiter`
- `--max-per-query` - Max results per query (default: 20)
- `--throttle` - Seconds between queries (default: 1.2)
- `--relevance-threshold` - Minimum relevance score (default: 1.0)

**Output Arguments:**
- `--out` - JSON output file (default: `web_jobs_ultimate.json`)
- `--txt-out` - Text summary file (default: `output/web_jobs_ultimate.txt`)
- `--csv-out` - CSV export of job postings (optional)

**Email Extraction Arguments:**
- `--extract-emails` - Enable email extraction from job postings
- `--emails-csv` - Path to save extracted emails (default: `output/found_emails.csv`)
- `--email-timeout` - Timeout for website fetching in seconds (default: 10)

**Email Sending Arguments:**
- `--send-emails` - Enable sending emails to extracted contacts
- Respects 50 email/day limit automatically
- Requires SendGrid or SMTP configuration

**Result Distribution:**
- `--email-to` - Send results summary to these email addresses
- `--email-top` - Number of top results to include (default: 10)
- `--email-subject` - Custom email subject line

## Output Files

All outputs are organized in the `output/` directory:

```
output/
├── web_jobs_ultimate.json          # All scraped job postings (JSON)
├── web_jobs_ultimate.txt           # Text summary of jobs
├── found_emails.csv                # Extracted and deduplicated emails
├── email_send_history.json         # Complete email sending history
└── .emails_sent_today.json         # Today's email count (for rate limiting)
```

## Email CSV Format

The `found_emails.csv` contains:
- `email` - Email address
- `domains` - Company domains where found
- `sources_count` - Number of job postings from this email
- `job_titles` - Related job titles
- `first_seen` - When email was first extracted
- `last_updated` - Last update time

## Environment Variables

Create a `.env` file in the project directory:

```bash
# For Gmail/Email notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# OR use SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
SMTP_USER=noreply@example.com

# For Search Engine APIs (optional)
GOOGLE_API_KEY=your_google_key
GOOGLE_CSE_ID=your_cse_id
SERPAPI_KEY=your_serpapi_key
```

### Gmail Setup for SMTP
1. Enable 2-Factor Authentication
2. Create an "App Password" at https://myaccount.google.com/apppasswords
3. Use the app password in `SMTP_PASSWORD`

## Rate Limiting

The system enforces:
- **50 emails per day maximum** - tracked in `.emails_sent_today.json`
- Daily counter resets at midnight
- If you run the scraper multiple times, emails sent on previous runs count toward the 50 limit

## Examples

### Example 1: Find IT Support Jobs and Extract Emails
```bash
python cli.py --keywords "IT Support,System Administrator" --locations "Chicago,Boston" --engines duckduckgo,indeed,simplyhired --extract-emails
```

Results saved to:
- `web_jobs_ultimate.json` - All job postings
- `output/web_jobs_ultimate.txt` - Readable summary
- `output/found_emails.csv` - All extracted emails

### Example 2: Find Jobs, Extract Emails, and Send Campaign (50 max)
```bash
python cli.py --keywords "Data Scientist" --locations "San Francisco" --engines serpapi,linkedin --extract-emails --send-emails --email-timeout 15
```

### Example 3: Custom Output Paths with Email Notification
```bash
python cli.py --keywords "Handyman,Painter" --locations "Denver" --engines duckduckgo,google_cse --out results/jobs.json --txt-out results/jobs_summary.txt --csv-out results/jobs.csv --extract-emails --emails-csv results/emails.csv --email-to boss@company.com --email-top 25
```

## Troubleshooting

**No emails found?**
- Increase `--max-per-query` to get more results
- Lower `--relevance-threshold` to 0.5
- Add more engines
- Check that job postings have accessible company websites

**Email sending fails?**
- Verify `SENDGRID_API_KEY` or SMTP credentials
- Check `--email-timeout` isn't too short
- Look at `output/email_send_history.json` for error details

**Rate limiting - can't send all emails?**
- Daily limit is 50 emails
- Run again tomorrow for more emails
- Check `.emails_sent_today.json` to see how many have been sent

**Website fetch errors?**
- Some sites may block automated scraping
- Try increasing `--email-timeout`
- Check robots.txt on target domains

## Advanced Features

### Scheduling Daily Runs

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 8 AM)
4. Set action to: `run_job_scraper.bat`

**Linux/Mac (Cron):**
```bash
# Daily at 8 AM
0 8 * * * cd /path/to/project && ./run_job_scraper.sh
```

### Using Different Environments

SendGrid example:
```bash
export SENDGRID_API_KEY="SG.xxx"
python cli.py --keywords "Developer" --locations "NYC" --extract-emails --send-emails
```

SMTP example:
```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your@gmail.com"
export SMTP_PASSWORD="app_password"
python cli.py --keywords "Developer" --locations "NYC" --extract-emails --send-emails
```

## API Keys & Services

### Free Options
- **DuckDuckGo**: Free, no key needed
- **Indeed**: Free, direct scraping
- **Greenhouse**: Free, direct scraping
- **Lever**: Free, direct scraping
- **Simply Hired**: Free, direct scraping

### Paid Services (Optional for Better Results)
- **SerpAPI**: $50/month for 100k searches - https://serpapi.com
- **Google Custom Search**: $100/month for 10k queries - https://cse.google.com
- **Bing Web Search**: Pay as you go - https://www.microsoft.com/en-us/bing/apis/bing-web-search-api

### Email Services (Optional)
- **SendGrid**: 100 free emails/day - https://sendgrid.com
- **Gmail SMTP**: Free with app password

## Performance Tips

1. **Start with free engines** (duckduckgo, indeed, greenhouse)
2. **Increase throttle** if getting blocked: `--throttle 2.5`
3. **Batch multiple searches** with multiple keywords
4. **Use CSV export** to avoid re-scraping
5. **Schedule off-peak hours** to avoid rate limits

## Limitations

- Email extraction success depends on website structure
- Some sites may block automated access (robots.txt/403)
- 50 email/day limit is enforced
- Results quality depends on search engine cooperation
- Some job boards require authentication

## Support

For issues, check:
1. `.env` file has correct credentials
2. `output/email_send_history.json` for error messages
3. Network connection and firewall settings
4. Website availability (some sites may be down)

---

**Version**: 2.0 (Email Extraction & Campaign Features)
**Last Updated**: December 2024
