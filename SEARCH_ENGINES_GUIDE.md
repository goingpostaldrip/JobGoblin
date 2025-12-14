# Search Engines & Job Sites Guide

## Overview
Your Job Scraper now displays **ALL available search engines and job sites** in a scrollable list, organized by category.

---

## 🎨 GUI Layout

### Scrollable Engine List
- **Height**: 200px scrollable area
- **Scrollbar**: Vertical scroll with modern styling
- **Categories**: 2 sections with visual separators
- **Icons**: Each engine has a unique emoji icon
- **Toggle Style**: Round switches (green for search engines, blue for job sites)

---

## 🔍 SEARCH ENGINES

These engines search the web for job listings using keywords and locations.

### 1. 🔍 **DuckDuckGo** (Free - Working ✓)
- **Status**: ✅ Currently Working
- **Type**: Free web search
- **Cost**: Free
- **API Key**: Not required
- **Default**: Enabled
- **Pros**: 
  - No API key needed
  - Privacy-focused
  - No rate limits
- **Cons**: 
  - May show CAPTCHA with heavy use
  - Can be blocked occasionally
- **Best For**: Quick searches, testing

### 2. 🔒 **Startpage** (Free - Privacy)
- **Status**: Available
- **Type**: Privacy-focused search
- **Cost**: Free
- **API Key**: Not required
- **Default**: Disabled
- **Pros**: 
  - Enhanced privacy
  - Anonymous searches
- **Cons**: 
  - Slower than other engines
  - May be blocked
- **Best For**: Privacy-conscious users

### 3. 🐍 **SerpAPI** (Paid - Requires API Key)
- **Status**: Available
- **Type**: Professional search API
- **Cost**: Paid (Free tier: 100 searches/month)
- **API Key**: Required
- **Default**: Disabled
- **Setup**: Set `SERPAPI_KEY` environment variable
- **Pros**: 
  - No CAPTCHA
  - Reliable
  - High success rate
- **Cons**: 
  - Requires paid subscription for production
- **Best For**: Production use, high volume
- **Website**: https://serpapi.com

### 4. 🔎 **Google CSE** (Paid - Requires API Key)
- **Status**: Available
- **Type**: Google Custom Search Engine
- **Cost**: Free tier limited (10,000 queries/day)
- **API Key**: Required
- **Default**: Disabled
- **Setup**: Set `GOOGLE_CSE_KEY` and `GOOGLE_CSE_ID` env vars
- **Pros**: 
  - Google's search quality
  - Programmable
- **Cons**: 
  - Complex setup
  - Limited free tier
- **Best For**: Google-specific searches
- **Website**: https://programmablesearchengine.google.com

### 5. 🅱️ **Bing** (Paid - Requires API Key)
- **Status**: Available
- **Type**: Microsoft Bing Search API
- **Cost**: Paid
- **API Key**: Required
- **Default**: Disabled
- **Setup**: Set `BING_SEARCH_KEY` environment variable
- **Pros**: 
  - Microsoft integration
  - Good coverage
- **Cons**: 
  - Requires Azure subscription
- **Best For**: Enterprise users with Azure
- **Website**: https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/

---

## 💼 JOB SITES (API-Based)

These sites are scraped directly using their APIs or RSS feeds - **NO BLOCKING!**

### 6. 💼 **Indeed**
- **Status**: Available (May be blocked)
- **Type**: Direct site scraper
- **Cost**: Free
- **Default**: Disabled
- **Method**: HTML scraping
- **Pros**: 
  - Huge job database
  - Well-known site
- **Cons**: 
  - Heavy anti-bot measures
  - Often blocked
  - May require proxies
- **Best For**: Large job searches with proxies

### 7. 🏢 **Greenhouse**
- **Status**: Available
- **Type**: ATS (Applicant Tracking System)
- **Cost**: Free
- **Default**: Disabled
- **Method**: Direct scraping
- **Pros**: 
  - Used by tech companies
  - Quality listings
- **Cons**: 
  - May be rate-limited
- **Best For**: Tech job searches

### 8. ⚙️ **Lever**
- **Status**: Available
- **Type**: ATS (Applicant Tracking System)
- **Cost**: Free
- **Default**: Disabled
- **Method**: Direct scraping
- **Pros**: 
  - Popular ATS
  - Startup-focused
- **Cons**: 
  - Limited to companies using Lever
- **Best For**: Startup job searches

### 9. 📋 **SimplyHired**
- **Status**: Available (May be blocked)
- **Type**: Job aggregator
- **Cost**: Free
- **Default**: Disabled
- **Method**: HTML scraping
- **Pros**: 
  - Large database
  - Aggregates from multiple sources
- **Cons**: 
  - May be blocked
  - Requires proxies
- **Best For**: Broad job searches

### 10. 🌐 **RemoteOK** (API - No Blocking) ⭐
- **Status**: ✅ Working
- **Type**: JSON API
- **Cost**: Free
- **Default**: Enabled
- **Method**: Official API endpoint
- **Pros**: 
  - ✅ No blocking - uses official API
  - Remote jobs focused
  - Fast and reliable
  - No CAPTCHA
- **Cons**: 
  - Remote jobs only
- **Best For**: Remote job searches
- **API**: https://remoteok.com/api

### 11. 🏠 **WeWorkRemotely** (RSS - No Blocking) ⭐
- **Status**: ✅ Working
- **Type**: RSS Feed
- **Cost**: Free
- **Default**: Enabled
- **Method**: RSS feed parsing
- **Pros**: 
  - ✅ No blocking - uses RSS feed
  - Programming jobs focused
  - Minimal rate limiting
  - Designed for consumption
- **Cons**: 
  - Remote jobs only
  - Fixed to programming category
- **Best For**: Remote developer jobs
- **RSS**: https://weworkremotely.com/categories/remote-programming-jobs.rss

### 12. 🚀 **Remotive** (API - No Blocking) ⭐
- **Status**: ✅ Working
- **Type**: REST API
- **Cost**: Free
- **Default**: Enabled
- **Method**: Official REST API
- **Pros**: 
  - ✅ No blocking - uses official API
  - High-quality remote jobs
  - Curated listings
  - No CAPTCHA
- **Cons**: 
  - Remote jobs only
  - Smaller database
- **Best For**: Quality remote job searches
- **API**: https://remotive.com/api/remote-jobs

---

## 📊 Selection Strategy

### ✅ Recommended Default Setup
**Enable these for best results without blocking:**
- ✅ DuckDuckGo (search engine)
- ✅ RemoteOK (API-based job site)
- ✅ WeWorkRemotely (RSS-based job site)
- ✅ Remotive (API-based job site)

### 🔧 With Proxies Setup
**If you have working proxies:**
- ✅ DuckDuckGo
- ✅ Indeed
- ✅ SimplyHired
- ✅ RemoteOK
- ✅ WeWorkRemotely
- ✅ Remotive

### 💰 Paid/Production Setup
**For high-volume, reliable scraping:**
- ✅ SerpAPI (requires API key)
- ✅ Google CSE (requires API key)
- ✅ RemoteOK
- ✅ WeWorkRemotely
- ✅ Remotive
- ✅ Indeed (with rotating proxies)

---

## 🎯 Quick Actions

### Select All Engines
- Click **"Select All"** button below the list
- Enables all 12 engines
- Use with caution - may hit rate limits

### Deselect All Engines
- Click **"Deselect All"** button
- Disables all engines
- Useful for starting fresh

### Scroll Through List
- Use mouse wheel to scroll
- Drag scrollbar for faster navigation
- All 12 engines visible in scrollable area

---

## ⚡ Performance Tips

### For Speed
1. **Enable only API-based sites** (RemoteOK, WeWorkRemotely, Remotive)
2. **Use 1-2 search engines** maximum
3. **Lower max results** (10-25 per query)

### For Coverage
1. **Enable all working engines**
2. **Use proxies** for Indeed/SimplyHired
3. **Higher max results** (50-100 per query)
4. **Multiple keyword variations**

### For Reliability
1. **Prioritize API-based sites** (marked with ⭐)
2. **Avoid blocked sites** unless using proxies
3. **Use paid APIs** for production
4. **Rotate proxies** regularly

---

## 🚨 Troubleshooting

### No Results from Search Engines?
- **Check**: Are proxies configured?
- **Try**: DuckDuckGo alone first
- **Issue**: May be CAPTCHA blocked
- **Solution**: Add proxies or use API-based sites

### No Results from Job Sites?
- **Check**: Internet connection
- **Try**: RemoteOK/WeWorkRemotely (should always work)
- **Issue**: Site may be down
- **Solution**: Enable multiple sites for redundancy

### Too Many Results?
- **Lower**: Max results per query (Options section)
- **Disable**: Some engines
- **Focus**: Specific keywords

### Results Too Slow?
- **Disable**: Slow/blocking sites (Indeed, SimplyHired)
- **Enable**: API-based sites only
- **Use**: Fewer engines simultaneously

---

## 📈 Visual Indicators

### Categories
- **═══ SEARCH ENGINES ═══** (Gold text)
  - Search the web for job listings
  - May encounter blocks/CAPTCHAs
  
- **═══ JOB SITES (API-Based) ═══** (Cyan text)
  - Direct job site scrapers
  - API/RSS-based sites won't block

### Toggle Colors
- **Green toggles** = Search engines
- **Blue toggles** = Job sites

### Status Labels
- **"Working ✓"** = Currently functioning
- **"No Blocking"** = Uses API/RSS (recommended)
- **"Requires API Key"** = Needs configuration
- **"Paid"** = Costs money (may have free tier)

---

## 🎓 Best Practices

1. **Start Simple**
   - Enable 2-3 engines
   - Test with single keyword
   - Verify results before scaling

2. **Mix Sources**
   - Combine search engines + job sites
   - Use API-based sites as primary
   - Search engines as supplementary

3. **Monitor Performance**
   - Check results per engine
   - Disable non-performing sources
   - Track which engines get blocked

4. **Adjust Based on Needs**
   - Remote jobs? → Enable RemoteOK, WeWorkRemotely, Remotive
   - Local jobs? → Enable Indeed, SimplyHired with proxies
   - Quality over quantity? → Use fewer, reliable sources
   - Coverage? → Enable all with proxies

---

**Last Updated**: December 9, 2025
**Total Engines Available**: 12 (5 search engines + 7 job sites)
**Recommended for No Blocking**: RemoteOK, WeWorkRemotely, Remotive
