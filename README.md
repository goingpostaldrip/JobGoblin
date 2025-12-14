# JOB SCRAPER ULTIMATE

**Complete job scraping, email extraction, and automated email campaign system.**

## 🚀 Quick Start

### Windows
```batch
quickstart.bat
# Then run:
run_job_scraper.bat
```

### Mac/Linux
```bash
chmod +x quickstart.sh
./quickstart.sh
```

## ✨ Features

### Core Job Scraping
- Multi-keyword, multi-location expansion into query permutations
- DuckDuckGo HTML scraping (no API key required) with throttle
- API engines: Google Custom Search (CSE), Bing Web Search, SerpAPI (robust paid)
- Site scrapers: Indeed, Greenhouse, Lever, SimplyHired
- Site-filtered web searches: LinkedIn, Glassdoor, ZipRecruiter (via SerpAPI `site:` queries)
- Relevance scoring with keyword boosts and threshold
- Outputs: JSON, TXT summary, optional CSV export

### 🆕 Email Extraction (NEW!)
- **Automatically scrapes job posting websites** to find contact emails
- **Smart email validation** - filters out noreply, notification, and bot emails
- **Deduplication** - removes duplicate emails and tracks all sources
- **CSV export** - saves all extracted emails to `output/found_emails.csv`
- Tracks domains, job titles, and sources for each email

### 🆕 Email Campaign Manager (NEW!)
- **50 email per day limit** - automatically enforced
- **Multiple email backends** - SendGrid or SMTP (Gmail, etc.)
- **Complete tracking** - logs every email sent with success/failure status
- **Daily reset** - counter resets automatically at midnight
- **Send history** - maintains complete log in `output/email_send_history.json`

## 📋 Usage Examples

### Interactive Mode (Easiest)
```batch
run_job_scraper.bat
```
Follow the prompts to:
1. Enter keywords (e.g., "Python Developer, Data Scientist")
2. Enter locations (e.g., "New York, San Francisco")
3. Choose search engines
4. Enable email extraction
5. Enable email sending (max 50/day)

### Command Line

**Basic scraping:**
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed
```

**With email extraction:**
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed --extract-emails
```

**Full pipeline (scrape + extract + send emails):**
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed --extract-emails --send-emails
```

**Send emails from existing CSV:**
```bash
python send_emails.py --csv output/found_emails.csv --subject "Job Opportunity" --limit 50
```

## 📁 Output Files

All files are saved to the `output/` directory:

```
output/
├── web_jobs_ultimate.json          # All scraped job postings
├── web_jobs_ultimate.txt           # Readable text summary
├── found_emails.csv                # Extracted and deduplicated emails ⭐
├── email_send_history.json         # Complete email sending history ⭐
└── .emails_sent_today.json         # Today's email count (rate limiting) ⭐
```

⭐ = New email features

## 🔧 Configuration

### Email Backend Setup

**Option 1: SendGrid (Recommended)**
```bash
# Free tier: 100 emails/day
export SENDGRID_API_KEY="SG.xxxxxxxxxxxxx"
export SMTP_USER="noreply@yourdomain.com"
```

**Option 2: Gmail SMTP**
```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your@gmail.com"
export SMTP_PASSWORD="app_password"  # Generate at myaccount.google.com/apppasswords
```

See `.env.example` for more configuration options.

## 📊 CSV Output Format

The `found_emails.csv` contains:
- **email** - Contact email address
- **domains** - Company domains where found
- **sources_count** - Number of job postings from this contact
- **job_titles** - Related job titles (up to 3)
- **first_seen** - When email was first extracted
- **last_updated** - Last update timestamp

## 🎯 Complete Examples

### Example 1: IT Support Jobs with Email Extraction
```bash
python cli.py \
  --keywords "IT Support,System Administrator" \
  --locations "Chicago,Boston,Denver" \
  --engines duckduckgo,indeed,simplyhired \
  --max-per-query 30 \
  --extract-emails \
  --verbose
```

### Example 2: Data Science Jobs + Email Campaign
```bash
python cli.py \
  --keywords "Data Scientist,Machine Learning Engineer" \
  --locations "San Francisco,Seattle" \
  --engines serpapi,linkedin \
  --extract-emails \
  --send-emails \
  --email-timeout 15
```

### Example 3: Custom Paths and Recipients
```bash
python cli.py \
  --keywords "Handyman,Painter,Landscaper" \
  --locations "Denver,Portland" \
  --engines duckduckgo,google_cse \
  --out results/jobs.json \
  --txt-out results/summary.txt \
  --csv-out results/jobs.csv \
  --extract-emails \
  --emails-csv results/emails.csv \
  --email-to boss@company.com \
  --email-top 25
```

## 🛠️ Command Line Arguments

### Search Options
- `--keywords` *(required)* - Comma-separated keywords
- `--locations` - Comma-separated locations (optional)
- `--engines` - Search engines to use (see list below)
- `--max-per-query` - Max results per query (default: 20)
- `--throttle` - Delay between queries in seconds (default: 1.2)
- `--relevance-threshold` - Minimum relevance score (default: 1.0)

### Output Options
- `--out` - JSON output path (default: `web_jobs_ultimate.json`)
- `--txt-out` - Text summary path (default: `output/web_jobs_ultimate.txt`)
- `--csv-out` - Optional CSV export path

### Email Extraction Options (NEW!)
- `--extract-emails` - Enable email extraction
- `--emails-csv` - Path for extracted emails CSV (default: `output/found_emails.csv`)
- `--email-timeout` - Website fetch timeout in seconds (default: 10)

### Email Sending Options (NEW!)
- `--send-emails` - Send emails to extracted contacts (50/day limit)
- Uses configured email backend (SendGrid or SMTP)

### Result Distribution
- `--email-to` - Send results summary to these addresses
- `--email-top` - Number of top results to include (default: 10)
- `--email-subject` - Custom email subject

## 🔍 Available Search Engines

### Free (No API Key)
- `duckduckgo` - DuckDuckGo search
- `indeed` - Indeed job board
- `greenhouse` - Greenhouse job board
- `lever` - Lever job board  
- `simplyhired` - Simply Hired job board

### Paid API Services
- `serpapi` - SerpAPI (recommended) - $50/month
- `google_cse` - Google Custom Search - $100/month  
- `bing` - Bing Web Search - Pay as you go
- `linkedin` - LinkedIn jobs (requires SerpAPI)
- `glassdoor` - Glassdoor (requires SerpAPI)
- `ziprecruiter` - ZipRecruiter (requires SerpAPI)

## ⚙️ Rate Limiting

The system enforces:
- **50 emails per day maximum** - tracked automatically
- Counter resets at midnight
- Multiple runs on same day share the 50-email limit
- Check `.emails_sent_today.json` for current count

## 📖 Documentation

- **FEATURES.md** - Complete feature documentation
- **.env.example** - Environment variable template
- **quickstart.bat/sh** - Quick start guides

## 🐛 Troubleshooting

**No emails found?**
- Increase `--max-per-query` to get more results
- Lower `--relevance-threshold` to 0.5
- Add more search engines
- Check that job postings have accessible company websites

**Email sending fails?**
- Verify `SENDGRID_API_KEY` or SMTP credentials in `.env`
- Check firewall/network settings
- Review `output/email_send_history.json` for error details

**Rate limit - can't send all emails?**
- Daily limit is 50 emails
- Run again tomorrow for remaining emails
- Check `.emails_sent_today.json` to see count

**Website fetch errors?**
- Some sites block automated scraping
- Increase `--email-timeout` value
- Check site's robots.txt

## 📦 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🔑 API Keys & Services

### Free Options (No Keys Needed)
- DuckDuckGo, Indeed, Greenhouse, Lever, SimplyHired

### Optional Paid Services (Better Results)
- **SerpAPI**: $50/month - https://serpapi.com
- **Google CSE**: $100/month - https://cse.google.com
- **Bing Search**: Pay as you go - https://www.microsoft.com/en-us/bing/apis

### Email Services
- **SendGrid**: 100 free emails/day - https://sendgrid.com
- **Gmail SMTP**: Free with app password

## 🚀 Next Steps

1. Copy `.env.example` to `.env` and configure your keys
2. Run `quickstart.bat` (Windows) or `quickstart.sh` (Mac/Linux)
3. Execute `run_job_scraper.bat` and follow prompts
4. Check `output/` folder for results
5. Send emails with `python send_emails.py --csv output/found_emails.csv`

## 📝 Version History

**v2.0** (December 2024)
- ✨ Email extraction from job postings
- ✨ Automated email campaigns with 50/day limit
- ✨ CSV export of extracted emails
- ✨ Complete email tracking and history
- ✨ Multiple email backend support (SendGrid + SMTP)

**v1.0** (Previous)
- Basic job scraping across multiple sources
- Search engine integration
- JSON/TXT/CSV outputs

---

**Need Help?** Check FEATURES.md for detailed documentation.
- `BING_API_KEY` for Bing Web Search.
- `SERPAPI_KEY` for SerpAPI (recommended for robust results).
- `SENDGRID_API_KEY` for optional email notifications.
Copy `.env.example` in this folder to `.env` and fill values.

## Output Schema
```json
{
  "query": "painter Pittsburgh PA",
  "engine": "duckduckgo",
  "title": "Example Painting Co - Careers",
  "url": "https://example.com/jobs/painter",
  "snippet": "We are hiring painters...",
  "ts": 1733000000,
  "hash": "<sha1 of title+url>"
}
```

## Safety / Rate Limiting
A 1.2s sleep is applied between DuckDuckGo queries to be polite. Increase if scaling.

## License
See root project `LICENSE`.
