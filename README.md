# JobGoblin - Lead Finder 🟢

**Professional job scraping and email extraction tool with modern GUI**

Created by **NERDY BIRD IT**  
📧 nerdybirdit@gmail.com  
📱 WhatsApp: +1 (412) 773-4245

---

## Features

- 🔍 **Multi-Engine Search** - DuckDuckGo, Google CSE, Bing, SerpAPI, and more
- 📧 **Email Extraction** - Automatically extract contact emails from job postings
- 💾 **Export Results** - Save scraped jobs to TXT files
- 📨 **Email Results** - Send job listings directly to clients via email
- 📊 **Archive & History** - Track all your scraping sessions
- ⚙️ **API Management** - Easy credential setup in GUI
- 🎨 **Modern Dark Theme** - Green/slime aesthetic

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/JobGoblin.git
cd JobGoblin
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python gui_app.py
```

---

## Configuration

### Search Engine APIs (Optional)
For enhanced search capabilities, configure API keys in the **Settings** tab:

- **Google Custom Search Engine (CSE)**
  - Google API Key
  - Custom Search Engine ID
  
- **Bing Search API**
  - Bing API Key
  
- **SerpAPI**
  - SerpAPI Key

### Email Sending (Optional)
To use the email results feature:

- **SendGrid** (Recommended)
  - SendGrid API Key
  - From Email
  
- **SMTP** (Gmail/Outlook)
  - SMTP User
  - SMTP Password
  - SMTP Server (default: smtp.gmail.com)
  - SMTP Port (default: 587)

---

## Usage

### Basic Job Scraping
1. Enter keywords (e.g., "remote developer, work from home")
2. Enter locations (optional, e.g., "New York, Los Angeles")
3. Select search engines (DuckDuckGo works without API keys)
4. Click **Start Scraping**
5. View results in the Results panel

### Export Results
- Click **💾 Export to TXT** to save jobs to a custom file
- Choose filename and location in the dialog

### Email Results
- Click **📧 Email Results** to send jobs to a client
- Enter recipient email and customize subject
- Requires email credentials configured in Settings

### Email Extraction
- Check "Extract Emails from Job Postings" option
- Emails are automatically saved to `output/found_emails.csv`
- View extracted emails in the Email Manager tab

---

## File Structure

```
JobGoblin/
├── gui_app.py              # Main GUI application
├── search_engines.py       # Search engine integrations
├── site_indeed.py          # Indeed scraper
├── site_greenhouse.py      # Greenhouse scraper
├── site_lever.py           # Lever scraper
├── site_simplyhired.py     # SimplyHired scraper
├── email_extractor.py      # Email extraction logic
├── email_manager.py        # Email tracking & export
├── email_sender.py         # Bulk email sending
├── normalize.py            # Job data normalization
├── cli.py                  # Command-line interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## Free Search Engines

**DuckDuckGo** works out of the box without any API keys! Other engines require paid API subscriptions.

---

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- See `requirements.txt` for all dependencies

---

## Support

Need help? Contact us:
- 📧 Email: nerdybirdit@gmail.com
- 📱 WhatsApp: +1 (412) 773-4245
- Or use the **Help & Support** tab in the app

---

## License

© 2025 NERDY BIRD IT. All rights reserved.

---

## Screenshots

*Modern dark theme with green accents*
*Multi-tab interface for easy navigation*
*Real-time progress tracking*

---

**Built with ❤️ by NERDY BIRD IT** 🟢
