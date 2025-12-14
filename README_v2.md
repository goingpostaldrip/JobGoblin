# 🎯 JOB SCRAPER ULTIMATE - Professional Edition v2.0

**Complete job scraping and email campaign system with professional GUI and command-line interfaces**

---

## ✨ What Can You Do?

### 🔍 Search for Jobs
- Search across **11+ job boards and search engines** simultaneously
- Support for keywords + locations
- Automatic deduplication
- Real-time results display

### 📧 Extract Contact Emails
- Automatically scrape emails from job posting websites
- Validate and deduplicate emails
- Export to CSV format
- Track domains and job titles per contact

### 📧 Email Campaigns
- Send emails to extracted contacts
- **50 emails/day limit** (enforced automatically)
- Complete campaign history and logging
- Support for SendGrid or SMTP backends

### 📁 Archive & History
- All scrapes automatically saved with timestamp
- Organized by date and time
- Searchable and filterable
- View full details on each past scrape

---

## 🚀 Quick Start (5 Minutes)

### Windows
```batch
launch_gui.bat
```

### macOS/Linux
```bash
./launch_gui.sh
```

### Web Search Immediately
1. Keep default keywords and locations
2. Click "Start Scraping"
3. See results in 1-2 minutes
4. Results auto-saved to `output/` folder

---

## 📖 How to Use

### Option 1: Professional GUI (Easiest)
**For most users** - Beautiful, colorful, intuitive interface
- Click buttons instead of typing commands
- Real-time progress and statistics
- View results immediately
- Manage email campaigns
- View scrape history

👉 **Read**: `GUI_QUICKSTART.md` (5 min) or `GUI_USER_GUIDE.md` (detailed)

### Option 2: Command Line (Advanced)
**For developers and automation** - Full control and scripting
```bash
python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed --extract-emails
```

👉 **Read**: `FEATURES.md` (all CLI options)

---

## 🎨 GUI Features

### 4 Main Tabs

1. **🔍 Job Scraper**
   - Easy keyword and location entry
   - Checkbox selection of 11+ search engines
   - Real-time progress bar
   - Live statistics (jobs, emails, time)
   - Color-coded results display
   - Save results with one click

2. **📁 Scrape Archive**
   - All past searches stored with timestamps
   - Most recent first
   - Search and filter by keyword/location/engine
   - Double-click to view full details
   - See statistics for each scrape

3. **📧 Email Manager**
   - View extracted emails
   - Send emails (50/day max, enforced)
   - Track daily statistics
   - View send history
   - Reset daily limit if needed

4. **⚙️ Settings**
   - Configure output directory
   - API key setup instructions
   - Email backend configuration
   - About information

---

## 🌐 Supported Job Boards

### Free (No API Key)
✅ **DuckDuckGo** - General web search
✅ **Indeed** - 50+ million job postings
✅ **SimplyHired** - Job aggregator
✅ **Greenhouse** - Startup careers
✅ **Lever** - Modern ATS careers

### Premium (Requires API Key)
💰 **LinkedIn Jobs** (via SerpAPI) - $50/month
💰 **Glassdoor** (via SerpAPI) - $50/month
💰 **ZipRecruiter** (via SerpAPI) - $50/month
💰 **Google Custom Search** - $100/month
💰 **Bing Web Search** - Pay-as-you-go

---

## 📁 Output Files

All results saved to `output/` directory:

| File | Format | Purpose |
|------|--------|---------|
| `web_jobs_ultimate.json` | JSON | All job data (complete) |
| `web_jobs_ultimate.txt` | TXT | Readable summary |
| `found_emails.csv` | CSV | Extracted emails |
| `scrape_archive.json` | JSON | Complete history |
| `email_send_history.json` | JSON | Campaign logs |

---

## 🔧 Installation

### Requirements
- Python 3.8 or later
- Stable internet connection
- ~100MB disk space for virtual environment

### Setup (First Time Only)

Both launcher scripts handle setup automatically:

```bash
# Windows
launch_gui.bat

# Linux/Mac
./launch_gui.sh
```

Or manually:
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python gui_app.py
```

---

## 📧 Email Configuration (Optional)

### SendGrid (Recommended)
1. Sign up free: https://sendgrid.com (100 free emails/day)
2. Create API key
3. Create `.env` file:
```
SENDGRID_API_KEY=SG.your_key_here
SMTP_USER=noreply@yourdomain.com
```

### SMTP (Gmail, Outlook, etc)
1. Gmail: Enable 2FA, create App Password
2. Create `.env` file:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your_app_password
```

**See** `.env.example` for more options.

---

## 🎯 Common Tasks

### Find Jobs in Your Area
```
1. Open GUI (launch_gui.bat or ./launch_gui.sh)
2. Enter keywords: "Python Developer, Data Scientist"
3. Enter locations: "New York, Los Angeles"
4. Click "Start Scraping"
5. Results in 3-5 minutes
```

### Extract & Email Contacts
```
1. Run scraper with "Extract emails" enabled (default)
2. Go to Email Manager tab
3. Review emails
4. Click "Send Emails (50 max)"
5. Emails sent respecting 50/day limit
```

### Archive & Search Past Scrapes
```
1. Click Archive tab
2. Use search box to filter by keywords/locations
3. Double-click entry to see full details
4. View statistics for each past scrape
```

---

## 💡 Tips for Best Results

### Get More Results
- Add more keywords (3-5 related terms)
- Add more locations (2-3 different areas)
- Increase max results per query (use slider)
- Add more search engines
- Run multiple times (different results each time)

### Find Better Email Matches
- More job postings = more emails found
- Use specific job titles (not generic)
- Target relevant locations
- Some sites block email scraping (normal)

### Speed Up Searches
- Lower max results (10 is faster than 100)
- Use fewer locations
- Use free engines only initially
- Test with 1-2 keywords first

---

## 🤖 Advanced Usage

### Command Line with All Options
```bash
python cli.py \
  --keywords "Python Developer,Data Scientist" \
  --locations "New York,Los Angeles,Chicago" \
  --engines duckduckgo,indeed,serpapi,linkedin \
  --max-per-query 50 \
  --extract-emails \
  --send-emails \
  --email-timeout 15 \
  --verbose
```

---

## 📚 Documentation

| Document | Purpose | Time |
|----------|---------|------|
| `GUI_QUICKSTART.md` | Get started in 5 minutes | 5 min |
| `GUI_USER_GUIDE.md` | Complete GUI reference | 20 min |
| `FEATURES.md` | All project features | 15 min |
| `PROJECT_SUMMARY.md` | Technical overview | 10 min |

---

## 🆘 Troubleshooting

### GUI Won't Start?
- Make sure Python 3.8+ installed: `python --version`
- Try: `pip install -r requirements.txt --upgrade`
- On Mac, try: `python3 gui_app.py`

### No Results Found?
- Increase "Max results per query" slider
- Try different keywords
- Add more search engines
- Check internet connection

### Emails Not Extracting?
- Some sites block automated scraping (normal)
- More job results = more emails found
- Takes 5-10 seconds per job posting

### Email Sending Fails?
- Check .env file exists in project root
- Verify API key is correct
- Look in `output/email_send_history.json` for error details

---

## 🌟 What Makes This Different?

### vs. Manual Job Searching
- ✅ Search 11+ sites simultaneously
- ✅ All results in one place
- ✅ Automatic deduplication
- ✅ No manual copy/pasting

### vs. Job Aggregators (Indeed, LinkedIn)
- ✅ Includes niche job boards
- ✅ Get email addresses for direct outreach
- ✅ No need to apply through job board
- ✅ Full data control

### vs. Email Scraper Tools
- ✅ Integrated job search + email extraction
- ✅ Open source (see all code)
- ✅ Complete email campaign management
- ✅ Daily limits and tracking

---

## 💻 System Requirements

### Minimum
- Python 3.8+
- 2GB RAM
- 100MB free disk space
- Internet connection

### Recommended
- Python 3.9+
- 4GB+ RAM
- 500MB+ free disk space
- Stable internet (fiber or cable)

---

## 🎉 Get Started Now!

### Windows Users
```batch
launch_gui.bat
```

### Mac/Linux Users
```bash
./launch_gui.sh
```

### Manual Start
```bash
python gui_app.py
```

---

## 🗺️ Project Files

```
📦 JOB SCRAPER ULTIMATE
├── 📁 output/                   ← All results saved here
├── 📁 __pycache__/              ← Python cache
├── launch_gui.bat               ← Windows launcher ⭐
├── launch_gui.sh                ← Linux/Mac launcher ⭐
├── gui_app.py                   ← GUI application
├── cli.py                       ← Command line interface
├── email_extractor.py           ← Email scraping module
├── email_manager.py             ← Email CSV & limits
├── email_sender.py              ← Email sending
├── requirements.txt             ← Python dependencies
├── .env.example                 ← Configuration template
├── README.md                    ← This file
├── GUI_QUICKSTART.md            ← 5-min quick start
├── GUI_USER_GUIDE.md            ← Comprehensive guide
├── FEATURES.md                  ← All features list
└── PROJECT_SUMMARY.md           ← Technical summary
```

---

**Version**: 2.0 Professional Edition
**Status**: ✅ Ready for Production
**Last Updated**: December 2025

Happy scraping! 🚀
