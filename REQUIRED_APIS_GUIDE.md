# Job Scraper Ultimate - Required APIs & Integration Guide

## Overview
Based on popular GitHub job scraper repositories, here are the essential APIs your app needs for complete functionality.

---

## 1. PAID APIs (High-Quality Results)

### 1.1 **Oxylabs Scraper API** (Recommended for Scale)
- **Website**: https://oxylabs.io
- **What it does**: Professional web scraping with Headless Browser, proxy rotation, JavaScript rendering
- **Endpoints**: 
  - Google Jobs Scraper
  - LinkedIn Jobs Scraper
  - Indeed Jobs Scraper
  - Glassdoor Scraper
- **Features**:
  - Real-time data retrieval
  - Custom parsing (XPath/CSS selectors)
  - Geo-location targeting (70+ countries)
  - Batch processing
  - Async/await support
- **Free Trial**: 1 week
- **Cost**: ~$50-500/month depending on volume
- **Auth**: Username/Password (BasicAuth)
- **Integration**: `requests.post("https://realtime.oxylabs.io/v1/queries", auth=("user", "pass"), json=payload)`

---

### 1.2 **RapidAPI Job Scraper APIs**
- **Website**: https://rapidapi.com (search "job" category)
- **Available APIs**:

#### A. LinkedIn Job Search API
- **Endpoint**: LinkedIn Job Search API (RapidAPI)
- **Features**: 10M+ jobs, no cookies needed
- **Rate Limit**: Tier dependent (100-5000 requests/month free)
- **Headers Required**:
  ```
  X-RapidAPI-Key: YOUR_KEY
  X-RapidAPI-Host: linkedin-job-search-api.p.rapidapi.com
  ```

#### B. Indeed Jobs Scraper API
- **Features**: Bypass 25-result limit, full job details
- **Rate Limit**: Free tier available
- **Auth**: RapidAPI Key

#### C. Glassdoor API
- **Features**: Reviews, salaries, company ratings
- **Rate Limit**: 100-500 requests/month free

#### D. Job Listings Aggregator API
- **Features**: Combines 8+ job platforms in one
- **Rate Limit**: Tier dependent

#### E. Naukri Jobs API (Asia)
- **Features**: Indian job market data
- **Rate Limit**: Free tier available

---

### 1.3 **Google Jobs API**
- **Website**: https://console.cloud.google.com
- **Setup**:
  1. Create Google Cloud Project
  2. Enable "Custom Search API"
  3. Create API Key in Credentials
  4. Create Custom Search Engine at cse.google.com
- **Requirements**:
  - `GOOGLE_API_KEY`: Your API key
  - `GOOGLE_CSE_ID`: Custom Search Engine ID
- **Limitations**: 100 free queries/day
- **Cost**: $5 per 1000 queries after free tier

---

### 1.4 **Bing Search API**
- **Website**: https://portal.azure.com
- **Setup**:
  1. Create Azure account
  2. Create "Bing Search v7" resource
  3. Copy API Key from settings
- **Requirements**:
  - `BING_API_KEY`: Your API key
- **Free Tier**: 3,000 requests/month
- **Cost**: $7-50/month for higher volumes

---

### 1.5 **SerpAPI** (Google SERP + Jobs)
- **Website**: https://serpapi.com
- **Features**: 
  - Google Jobs results
  - LinkedIn Jobs
  - Google Scholar
  - Multi-location support
- **Free Tier**: 100 searches/month
- **Pricing**: Pay-as-you-go ($0.006-0.08 per search)
- **Requirements**:
  - `SERPAPI_KEY`: Your API key
- **Integration**:
  ```python
  params = {
      "q": "python developer remote",
      "location": "San Francisco",
      "api_key": SERPAPI_KEY
  }
  response = requests.get("https://serpapi.com/search", params=params)
  ```

---

## 2. FREE OPEN-SOURCE LIBRARIES

### 2.1 **JobSpy** (Python Library)
- **GitHub**: https://github.com/asadintwala/jobspy_scraper_api
- **What it scrapes**: LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt, Naukri
- **Installation**: `pip install python-jobspy`
- **Usage**:
  ```python
  from jobspy import scrape_jobs
  
  jobs = scrape_jobs(
      site_name=["indeed", "linkedin"],
      search_term="software engineer",
      location="San Francisco, CA",
      results_wanted=50,
  )
  ```
- **Advantages**: No API keys needed, covers multiple sites
- **Limitations**: Rate limiting (use proxies), slower than APIs

---

### 2.2 **Oxylabs Free Google Jobs Scraper**
- **GitHub**: https://github.com/oxylabs/how-to-scrape-google-jobs
- **What it does**: Scrapes Google Jobs for free
- **No API key required**
- **Limitations**: Single-threaded, slower than API

---

## 3. EMAIL EXTRACTION APIs

### 3.1 **Hunter.io**
- **Website**: https://hunter.io
- **Features**: Find email addresses by domain
- **Endpoint**: `https://api.hunter.io/v2/email-finder`
- **Free Tier**: 100 requests/month
- **Requirements**:
  - `HUNTER_API_KEY`: Your API key
- **Usage**:
  ```python
  params = {
      "domain": "company.com",
      "api_key": HUNTER_API_KEY
  }
  response = requests.get("https://api.hunter.io/v2/email-finder", params=params)
  ```

### 3.2 **Clearbit**
- **Website**: https://clearbit.com
- **Features**: Email lookup, company enrichment
- **Free Tier**: Limited
- **Cost**: $100+/month

### 3.3 **RocketReach**
- **Website**: https://rocketreach.com
- **Features**: Professional contact database
- **Cost**: $50+/month

---

## 4. PROXY SERVICES (for rate limit bypass)

### 4.1 **Bright Data (formerly Luminati)**
- **Website**: https://brightdata.com
- **Features**: Rotating proxies, Headless Browser
- **Free Trial**: $0.1 credit
- **Best for**: LinkedIn, Indeed (aggressive blockers)

### 4.2 **Oxylabs Proxies**
- **Included with** Oxylabs Scraper API
- **Unlimited rotation**

### 4.3 **Smartproxy**
- **Website**: https://smartproxy.com
- **Cost**: $10-50/month for residential proxies
- **Features**: SOCKS5, HTTP/HTTPS support

### 4.4 **Free Proxy Lists** (Built-in to your app)
- GitHub sources you're already using:
  - TheSpeedX/PROXY-List (46k+ proxies)
  - Proxifly/free-proxy-list
  - monosans/proxy-list
  - clarketm/proxy-list

---

## 5. EMAIL SENDING APIs

### 5.1 **SendGrid** (Recommended - already in your app)
- **Website**: https://sendgrid.com
- **Free Tier**: 100 emails/day
- **Paid Tier**: $20/month for 40,000 emails
- **Requirements**:
  - `SENDGRID_API_KEY`: Your API key
- **Already integrated in your app** ✓

### 5.2 **Gmail SMTP** (Free - already in your app)
- **Requirements**:
  - Enable 2-Step Verification on Google Account
  - Generate App-specific password
  - `SMTP_HOST`: smtp.gmail.com
  - `SMTP_PORT`: 587
  - `SMTP_USER`: your@gmail.com
  - `SMTP_PASSWORD`: 16-char app password
- **Already integrated in your app** ✓

---

## 6. RECOMMENDED SETUP FOR YOUR APP

### **Tier 1: Free (No API Keys Needed)**
- ✓ DuckDuckGo (already using)
- ✓ JobSpy library (add this)
- ✓ Email extraction via regex + web scraping (already doing)
- ✓ Free proxies (already using)

### **Tier 2: Freemium (Easy Setup)**
- SerpAPI ($6-50/month) - Google Jobs + LinkedIn
- RapidAPI accounts (free tier for many APIs)
- Hunter.io (100 emails/month free)

### **Tier 3: Professional (Scale)**
- Oxylabs Scraper API ($50-500/month) - Most reliable
- Bright Data Proxies ($100+/month) - Best for hard targets
- Clearbit ($100+/month) - Company enrichment

---

## 7. QUICK API SETUP CHECKLIST

### To Add Each API to Your App:

```
1. SerpAPI
   - Sign up: https://serpapi.com
   - Get API key: Settings > API Keys
   - Add to .env: SERPAPI_KEY=xxx
   - Update .env in GUI

2. RapidAPI (Multi-API via one account)
   - Sign up: https://rapidapi.com
   - Subscribe to "LinkedIn Job Search API"
   - Get key: Settings > API Keys
   - Add to .env: RAPIDAPI_KEY=xxx
   - Header will auto-use this

3. Google CSE
   - Create project: https://console.cloud.google.com
   - Enable Custom Search API
   - Create search engine: https://cse.google.com
   - Add to .env:
     GOOGLE_API_KEY=xxx
     GOOGLE_CSE_ID=yyy

4. Bing
   - Azure account: https://portal.azure.com
   - Create "Bing Search" resource
   - Copy key to .env:
     BING_API_KEY=xxx
```

---

## 8. ESTIMATED MONTHLY COSTS (Basic Setup)

| Service | Free Tier | Monthly Cost |
|---------|-----------|--------------|
| SerpAPI | 100 searches | $15-50 |
| RapidAPI | 100-500/month | FREE |
| Google CSE | 100 queries | $5-20 |
| Bing | 3,000 requests | FREE-$10 |
| Oxylabs | - | $50-500 |
| Hunter.io | 100 searches | FREE-50 |
| **TOTAL** (Recommended) | - | **$20-80/mo** |

---

## 9. YOUR APP'S CURRENT CAPABILITIES

✓ DuckDuckGo (free, no key needed)
✓ Startpage (free, no key needed)
✓ Email extraction via web scraping
✓ Email sending (Gmail SMTP + SendGrid)
✓ Proxy rotation (free GitHub sources)
✓ GUI with settings tab for API keys

---

## 10. RECOMMENDED NEXT STEPS

1. **Add SerpAPI** (easiest, $5-15/month)
   - Already has code in your app, just needs API key

2. **Install JobSpy** (free library)
   - Covers LinkedIn, Indeed, Glassdoor without APIs
   - Command: `pip install python-jobspy`

3. **Set up Hunter.io** (free email finding)
   - 100 emails/month free
   - Better accuracy than regex

4. **Scale to Oxylabs** (when you need volume)
   - Most reliable for 1000+ daily scrapes
   - Worth it once you prove the concept

