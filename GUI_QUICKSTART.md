# 🚀 Quick Start - GUI Version

## Installation & First Run

### Windows
1. Double-click **`launch_gui.bat`**
2. First time setup runs automatically
3. GUI opens in ~30 seconds

### macOS/Linux
1. Open terminal in project folder
2. Run: `./launch_gui.sh`
3. Or: `python gui_app.py`
4. GUI opens in ~10 seconds

## Your First Scrape (5 Minutes)

### Step 1: Enter Search Terms
- **Keywords**: "Python Developer" (or your desired job title)
- **Locations**: "New York" (or leave blank for nationwide)

### Step 2: Select Search Engines
- Free options already checked by default ✅
- DuckDuckGo, Indeed, SimplyHired (free & effective)

### Step 3: Click Start Scraping
- Status shows progress in real-time
- Results appear as they're found
- Takes 1-5 minutes depending on results

### Step 4: Save Results
- Automatically saved when done
- Manually click "💾 Save Results" for backup
- Files in `output/` folder

## Where Are My Results?

**In the GUI:**
- See results in the "📋 Results" panel
- Color-coded for easy reading

**In Files:**
- `output/web_jobs_ultimate.json` - All data
- `output/web_jobs_ultimate.txt` - Easy to read
- `output/found_emails.csv` - Just the emails
- `output/scrape_archive.json` - All past scrapes

## Archive - View Past Scrapes

Click the **📁 Scrape Archive** tab to see:
- All previous searches
- Date & time of each scrape
- How many jobs/emails found
- Double-click to view full details

## Next Steps

### Get Better Results
1. Try different keywords: "Data Scientist", "ML Engineer"
2. Add multiple locations: "New York, Los Angeles, Chicago"
3. Increase max results slider: Try 50 instead of 25
4. Run multiple times: Different results each time

### Extract & Send Emails
1. ✓ Enable "Extract contact emails" (default on)
2. ✓ Click "Start Scraping"
3. Go to **📧 Email Manager** tab
4. Click **📊 View Email CSV** to see emails found
5. Click **📧 Send Emails** to email contacts (max 50/day)

### Use Premium Search Engines
1. Get free trial API keys:
   - SerpAPI: 100 free searches
   - Google CSE: Free tier available
   - Bing: Free tier available
2. Add to `.env` file (see Settings tab for instructions)
3. Enable in GUI
4. Get much better results!

## Tips

🎯 **Most Effective Setup:**
- Keywords: 3-5 related job titles
- Locations: 2-3 major cities
- Engines: DuckDuckGo, Indeed, SimplyHired
- Max results: 25-50
- Time: 3-10 minutes

📧 **Email Campaign:**
- Extract emails ✓
- Review in Email Manager
- Send 50/day max (respects daily limit)
- Check history in `email_send_history.json`

💰 **Want Even Better Results?**
- Add SerpAPI ($50/month for 100k searches)
- Gets LinkedIn, Glassdoor, ZipRecruiter results
- 10x more coverage than free options

## Common Questions

**Q: How many results will I get?**
A: 10-100+ per keyword/location combo depending on job market

**Q: Can I send emails automatically?**
A: Yes! Enable email extraction, then use Email Manager (50/day limit)

**Q: What if I don't get results?**
A: Try different keywords or increase max results slider

**Q: Can I schedule daily scrapes?**
A: Currently manual. You can run GUI once per day, or use CLI with Windows Task Scheduler

**Q: How much does this cost?**
A: Completely free with free search engines! Optional paid APIs for premium results.

## Troubleshooting

**GUI won't start?**
- Make sure Python 3.8+ installed
- Try: `pip install -r requirements.txt`

**No results found?**
- Increase "Max results per query" slider
- Try different keywords
- Check internet connection

**Emails not extracting?**
- Some sites don't have public email
- More results = more emails found
- Takes ~5-10 seconds per job posting

**For detailed help:**
- See `GUI_USER_GUIDE.md` (comprehensive)
- See `FEATURES.md` (all features)

---

**Ready?** Double-click `launch_gui.bat` or run `./launch_gui.sh` and start scraping! 🎉
