## 🎨 JOB SCRAPER ULTIMATE - GUI Edition

Professional, colorful desktop application for comprehensive job scraping and email campaign management.

---

## ✨ Features

### 🔍 Smart Job Scraper Tab
- **Easy Site Selection**: Checkboxes for 11+ different job boards and search engines
- **Quick Select**: "Select All" / "Deselect All" buttons for convenience
- **Flexible Search**: Multiple keywords and locations support
- **Advanced Options**:
  - Adjustable max results per query (10-100)
  - Email extraction toggle
  - Email sending toggle (50/day limit enforced)
  - Real-time progress bars and status updates

### 📊 Scrape Archive Tab
- **Complete History**: All past scrapes stored with timestamps
- **Organized by Date & Time**: Most recent scrapes shown first
- **Quick Filtering**: Search by keywords, locations, or engines
- **Detailed View**: Click any entry to see full results and statistics
- **Easy Clearing**: Delete entire archive if needed

### 📧 Email Manager Tab
- **Real-time Statistics**: 
  - Total emails extracted
  - Emails sent today vs 50-day limit
  - Remaining emails available
- **One-Click Sending**: Send to all extracted emails (respects 50/day limit)
- **CSV Viewer**: View all extracted emails with details
- **Limit Management**: Reset daily limit if needed

### ⚙️ Settings Tab
- **Output Directory Configuration**: Choose where files are saved
- **API Keys Guide**: Clear instructions for setting up search engine APIs
- **Email Backend Setup**: Instructions for SendGrid and SMTP
- **About Information**: Version and project details

---

## 🚀 Getting Started

### Windows
```batch
launch_gui.bat
```

### macOS/Linux
```bash
./launch_gui.sh
```

Or manually:
```bash
python gui_app.py
```

---

## 📖 Step-by-Step Usage

### 1. **Configure Your Search**

#### Keywords
Enter job titles or skills you want to find (comma-separated):
```
Python Developer, Data Scientist, Machine Learning Engineer
```

#### Locations
Enter cities, regions, or countries (comma-separated):
```
New York, Los Angeles, San Francisco
```

Leave blank to search nationally/globally.

#### Select Search Engines

**Free Options (No API Key):**
- ✅ DuckDuckGo - General web search
- ✅ Indeed - Major job board
- ✅ SimplyHired - Job aggregator
- ✅ Greenhouse - Startup careers
- ✅ Lever - Modern job board

**Paid APIs (Better Results):**
- 💰 SerpAPI - $50/month (recommended)
- 💰 Google Custom Search - $100/month
- 💰 Bing Search - Pay-as-you-go

**Site-Filtered Searches** (requires SerpAPI):
- LinkedIn Jobs
- Glassdoor
- ZipRecruiter

**💡 Tip**: Start with free engines (DuckDuckGo, Indeed, SimplyHired) to test, then add paid APIs for better coverage.

### 2. **Adjust Options**

**Max Results Per Query**: Slider to set 10-100 results per search
- Lower (10-20): Faster, fewer results
- Higher (50-100): More thorough, slower

**Extract Contact Emails**: ✓ Enabled by default
- Automatically finds company emails from job posting websites
- Saves to `found_emails.csv`

**Send Emails**: ⚪ Optional, disabled by default
- Sends emails to extracted contacts (max 50/day)
- Requires SendGrid or SMTP configuration
- See **Settings** tab for setup

### 3. **Start Scraping**

Click the **🚀 Start Scraping** button to begin.

The GUI will show:
- Current query being searched
- Real-time progress bar
- Live statistics (jobs found, emails extracted, elapsed time)
- Results appearing in the results panel

Click **⛔ Stop** to cancel at any time.

### 4. **View Results**

Results display in real-time with color-coded formatting:
- **Blue**: Job titles
- **Purple**: URLs
- **Orange**: Search engine source
- **Green**: Extracted emails

**Features:**
- Scrollable list with all details
- Clean formatting for readability
- Sample of extracted emails shown at bottom

### 5. **Save Results**

Click **💾 Save Results** to export:
- `output/web_jobs_ultimate.json` - All data (JSON)
- `output/web_jobs_ultimate.txt` - Readable summary
- `output/found_emails.csv` - Extracted emails only

Automatically saved when scraping completes!

---

## 📁 Archive Tab - Scrape History

### View Past Scrapes
All previous scrapes are automatically archived with:
- Date and time of scrape
- Keywords searched
- Locations queried
- Search engines used
- Number of jobs found
- Number of emails extracted

### Search Archive
Use the search box to filter by:
- Keywords
- Locations
- Engine names
- Any combination

### View Details
Double-click any entry to see:
- Complete scrape information
- Sample of results (first 10 jobs)
- Full statistics

### Clear Archive
Use the "🗑️ Clear Archive" button to delete all history (cannot be undone).

---

## 📧 Email Manager Tab

### Monitor Email Campaign

**Statistics Panel Shows:**
- **Total Emails**: All unique emails extracted
- **Sent Today**: X/50 - How many sent vs daily limit
- **Remaining**: How many more can be sent today

### Send Emails

**Requirements:**
- Must have extracted emails first (run scraper with extraction enabled)
- SendGrid API key OR SMTP credentials configured (.env file)

**Process:**
1. Click **📧 Send Emails (50 max)**
2. Confirm you want to send
3. Emails are sent at 1/second rate (respects daily limit)
4. View results of send attempt

**Daily Limit:**
- Maximum 50 emails per day (enforced)
- Resets at midnight
- Track all sends in `email_send_history.json`

### View Emails
Click **📊 View Email CSV** to see all extracted emails with:
- Email address
- Company domains found at
- Related job titles
- When email was discovered

### Manage Daily Limit

If you need to test or have legitimate needs:
1. Click **🔓 Reset Daily Limit**
2. Confirm the reset
3. You'll have 50 more emails to send today

---

## ⚙️ Settings Tab

### Output Directory
Change where all files are saved:
1. Default: `output/` folder
2. Click **Browse** to choose custom location
3. All results, archive, emails saved there

### API Keys Configuration

#### Setup SendGrid (Recommended)
1. Sign up free: https://sendgrid.com (100 free emails/day)
2. Create an API key
3. Create `.env` file with:
```
SENDGRID_API_KEY=SG.your_api_key_here
SMTP_USER=noreply@yourdomain.com
```

#### Setup SMTP (Gmail, Outlook, etc)
1. **Gmail**: Enable 2FA, create App Password
   - https://myaccount.google.com/apppasswords
2. Create `.env` file:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app_password_here
```

#### Setup Search Engine APIs (Optional)
```
# Google Custom Search
GOOGLE_API_KEY=your_key
GOOGLE_CSE_ID=your_cse_id

# SerpAPI (recommended for LinkedIn, Glassdoor, etc)
SERPAPI_KEY=your_key

# Bing Web Search
BING_API_KEY=your_key
```

**Note**: Copy `.env.example` to `.env` and fill in your keys.

---

## 💾 Output Files

All files saved to `output/` directory:

```
output/
├── web_jobs_ultimate.json          # All job postings (JSON)
├── web_jobs_ultimate.txt           # Text summary
├── found_emails.csv                # Extracted emails (CSV)
├── scrape_archive.json             # Complete history
├── email_send_history.json         # Email campaign log
└── .emails_sent_today.json         # Today's send count
```

### File Formats

**JSON** - Complete structured data, includes all fields
**TXT** - Simple text list for quick reading
**CSV** - Spreadsheet format, easily opened in Excel

---

## 🎯 Common Workflows

### Workflow 1: Quick Job Search
1. Enter keyword (e.g., "Python Developer")
2. Keep free engines checked (DuckDuckGo, Indeed)
3. Click "Start Scraping"
4. Wait for results
5. Click "Save Results"

**Time**: ~2-3 minutes | **Results**: 50-200+ jobs

### Workflow 2: Targeted Location Search
1. Enter keywords: "Data Scientist, ML Engineer"
2. Enter locations: "San Francisco, Seattle, Portland"
3. Select Indeed, SimplyHired (free + relevant)
4. Set max results to 50
5. Enable email extraction
6. Click "Start Scraping"

**Time**: ~5-10 minutes | **Results**: 100-300 jobs, 50-100 emails

### Workflow 3: Email Campaign
1. Run scraper with email extraction enabled
2. Go to Email Manager tab
3. Review extracted emails (check CSV)
4. Click "Send Emails (50 max)"
5. Check statistics to confirm
6. Check `email_send_history.json` for logs

**Emails Sent**: Up to 50/day

### Workflow 4: Comprehensive Search (All Engines)
1. Click "Select All" for engines
2. Requires all API keys configured
3. Enter broad keywords
4. Set max results to 30 (more thorough)
5. Run overnight or during off-hours
6. Check archive next day

**Time**: 30+ minutes | **Results**: 500+ jobs, 100-200+ emails

---

## 🔍 Tips & Tricks

### Get Better Results
1. **Use Multiple Keywords**: More keywords = more matches
2. **Add Locations**: Even if searching nationally, be specific
3. **Use Multiple Engines**: Free engines find different results
4. **Pay for APIs**: SerpAPI finds best LinkedIn/Glassdoor/Indeed results
5. **Run Multiple Times**: Each run may find different jobs

### Speed Up Searches
1. Lower "Max results per query" (10 is faster than 100)
2. Use fewer locations (e.g., 1-2 instead of 5)
3. Use fewer engines (focus on most relevant)
4. Disable email extraction if not needed
5. Run during off-peak hours

### Email Sending Best Practices
1. **Start Small**: Send 10 emails first, check deliverability
2. **Use Professional Email**: Not personal Gmail if possible
3. **Personalize**: Consider using SMTP with your own email
4. **Monitor Results**: Check `email_send_history.json` for bounces
5. **Respect Limits**: 50/day helps maintain reputation
6. **Stagger Sends**: Spread over 1-2 hours, not all at once

### Troubleshooting
- **No results found?**
  - Increase "Max results per query"
  - Try different/broader keywords
  - Add more search engines
  - Check API keys are working

- **Emails not extracting?**
  - Some company sites don't have public contact emails
  - Try increasing results to get more job postings
  - Check website accessibility (some block scrapers)

- **Email sending failing?**
  - Verify API key in .env file
  - Check .env file exists in project root
  - Look in `email_send_history.json` for error details
  - Try sending individual test email first

---

## 🌐 Supported Job Boards

### Free (No API Key)
✅ DuckDuckGo - General web search
✅ Indeed - 50+ million jobs
✅ SimplyHired - Job aggregator
✅ Greenhouse - Startup careers site
✅ Lever - Modern ATS/Careers site

### Paid (With API)
💰 LinkedIn Jobs (via SerpAPI)
💰 Glassdoor (via SerpAPI)
💰 ZipRecruiter (via SerpAPI)
💰 Google Custom Search (broad coverage)
💰 Bing Web Search (broad coverage)

### Coverage
- Local job boards
- Company career sites
- Freelance platforms
- Contract job sites
- Startup boards

---

## 🔐 Privacy & Compliance

### Important Notes
1. **Respect robots.txt**: System respects site crawling policies
2. **Rate Limiting**: 1-2 second delays between requests
3. **Email Compliance**: Only contact jobs found (implied consent)
4. **Data Privacy**: All data stored locally, nothing uploaded
5. **Terms of Service**: Review job board ToS before scraping

### Responsible Use
- Don't overload servers (use rate limiting)
- Respect daily email limits
- Don't spam contacts
- Use professional email addresses
- Honor unsubscribe requests

---

## 📊 Performance Tips

### System Requirements
- Minimum: Python 3.8, 2GB RAM
- Recommended: Python 3.9+, 4GB RAM
- Network: Stable internet connection

### Expected Times
- Small search (1 keyword, 1 location): 1-2 minutes
- Medium search (3-5 keywords, 2-3 locations): 5-10 minutes
- Large search (10+ keywords, 5+ locations): 15-30 minutes
- Very large (all engines, all options): 30-60+ minutes

### Results Volumes
- Per keyword/location: 5-100 jobs
- With 10 combinations: 50-1000 jobs
- Email extraction: 5-20% of jobs have extractable emails

---

## 🎓 Video Tutorial Workflow

(Future: Add links to tutorial videos)

---

## 📞 Support

For issues:
1. Check `.env` file is in project root with API keys
2. Review `output/email_send_history.json` for errors
3. Check internet connection
4. Verify Python 3.8+ installed
5. Try: `pip install -r requirements.txt --upgrade`

---

## 🎉 Advanced Features Coming Soon

- 📊 Advanced analytics dashboard
- 🤖 AI-powered email personalization
- 📱 Mobile app version
- 🌍 Multi-language support
- 🎨 More theme options
- ⏰ Scheduled scraping
- 💾 Database integration

---

**Version**: 2.0 GUI
**Last Updated**: December 2025
**Status**: Professional Edition Ready for Use ✅
