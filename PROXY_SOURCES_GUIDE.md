# Proxy Sources Guide

## Overview
Your Job Scraper now includes **8 different proxy sources** with automatic discovery and validation. This gives you multiple routes to obtain working proxies for bypassing anti-bot measures.

---

## 🔥 GitHub-Based Sources (Most Reliable)

### 1. **TheSpeedX/PROXY-List**
- **Update Frequency**: Regularly updated
- **Proxy Types**: HTTP, SOCKS4, SOCKS5
- **Quality**: High - one of the most popular proxy lists on GitHub
- **URL**: https://github.com/TheSpeedX/PROXY-List
- **Fetches From**:
  - `http.txt` - HTTP proxies
  - `socks4.txt` - SOCKS4 proxies
  - `socks5.txt` - SOCKS5 proxies

### 2. **Proxifly Free Proxy List** ⭐ NEW
- **Update Frequency**: Every 5 minutes (most frequent!)
- **Proxy Types**: HTTP, HTTPS, SOCKS4, SOCKS5
- **Quality**: Excellent - all proxies are validated before listing
- **Features**:
  - 5,000+ proxies from 91 countries
  - Speed-tested
  - Duplicates removed
  - HTTPS proxies verified with SSL/TLS
- **URL**: https://github.com/proxifly/free-proxy-list
- **Fetches From**:
  - Uses CDN for faster access
  - `http/data.txt` - HTTP proxies
  - `socks4/data.txt` - SOCKS4 proxies
  - `socks5/data.txt` - SOCKS5 proxies

### 3. **Zebbern/Proxy-Scraper** ⭐ NEW
- **Update Frequency**: Every hour
- **Proxy Types**: HTTP, HTTPS, SOCKS4, SOCKS5
- **Quality**: Good - updated hourly with validation
- **URL**: https://github.com/zebbern/Proxy-Scraper
- **Fetches From**:
  - `http.txt` - HTTP proxies
  - `https.txt` - HTTPS proxies
  - `socks4.txt` - SOCKS4 proxies
  - `socks5.txt` - SOCKS5 proxies

### 4. **ProxyList (by Haitham Aouati)** ⭐ NEW
- **Update Frequency**: Every hour
- **Proxy Types**: HTTP, HTTPS, SOCKS4, SOCKS5
- **Quality**: Good - verified before listing
- **Features**:
  - Global proxies from various locations
  - Speed-tested
  - Duplicates filtered
- **URL**: https://github.com/haithamaouati/ProxyList
- **Fetches From**:
  - `http.txt` - HTTP proxies
  - `https.txt` - HTTPS proxies
  - `socks4.txt` - SOCKS4 proxies
  - `socks5.txt` - SOCKS5 proxies

### 5. **Ninjah (by Haitham Aouati)** ⭐ NEW
- **Update Frequency**: Every hour
- **Note**: Uses same proxy sources as ProxyList (same author)
- **URL**: https://github.com/haithamaouati/Ninjah

---

## 🌐 Web Scraper Sources

### 6. **free-proxy-list.com**
- **Method**: HTML scraping
- **Proxy Types**: HTTP, HTTPS
- **Quality**: Variable
- **Note**: May be slower due to HTML parsing

### 7. **us-proxy.org**
- **Method**: HTML scraping
- **Proxy Types**: HTTP
- **Quality**: Variable
- **Note**: US-focused proxies

### 8. **freeproxylists.net**
- **Method**: HTML scraping
- **Proxy Types**: HTTP
- **Quality**: Variable
- **Note**: May have outdated proxies

---

## 🎯 How Auto-Discovery Works

1. **Fetch from All Sources**
   - The app queries all 8 sources simultaneously
   - Each source provides a batch of proxies
   - Duplicates are automatically removed

2. **Validation**
   - Each proxy is tested against `httpbin.org/ip`
   - Only working proxies are saved
   - Timeout: 5 seconds per test

3. **Priority Order**
   - GitHub sources are tried FIRST (most reliable)
   - Web scraper sources are backup
   - Order of GitHub sources:
     1. TheSpeedX/PROXY-List
     2. Proxifly (fastest updates)
     3. Zebbern/Proxy-Scraper
     4. ProxyList
     5. Ninjah

---

## 📊 Usage in GUI

### Auto-Discovery
1. Open **Proxy Manager** tab
2. Click **"Auto-Discover Proxies"**
3. Set limit (e.g., 10 proxies)
4. Click **"Start Discovery"**
5. Wait for validation (shows progress)
6. Working proxies are automatically saved

### Manual Proxy Management
- **Add**: Input proxy URL manually
- **Remove**: Select and delete
- **Enable/Disable**: Toggle individual proxies
- **Test**: Validate specific proxies
- **Clear All**: Remove all proxies

---

## ✅ Best Practices

### For Maximum Success
1. **Use GitHub sources** - Most reliable and frequently updated
2. **Proxifly is fastest** - Updated every 5 minutes
3. **Test before use** - Always validate proxies
4. **Rotate regularly** - Get fresh proxies every few hours
5. **Consider paid proxies** - For production use

### Expected Results
- **GitHub sources**: 50-80% success rate
- **Web scrapers**: 20-40% success rate
- **Free proxies**: May be slow or unreliable
- **Paid proxies**: 95%+ success rate (recommended for production)

---

## ⚠️ Important Notes

### Proxy Reliability
- Free proxies may log your browsing history
- Not recommended for sensitive operations
- May be slower than direct connections
- Can be blocked by websites at any time

### Legal & Ethical Use
- Use proxies responsibly and ethically
- All proxies are publicly available
- Any illegal use is solely your responsibility
- Respect website terms of service

### Fallback System
- If proxy fails → automatically retries without proxy
- No more stuck searches
- Graceful degradation ensures continuous operation

---

## 🚀 Performance Tips

1. **Start with 5-10 proxies** - Don't fetch too many at once
2. **Test regularly** - Proxies die frequently
3. **Clear dead proxies** - Remove non-working ones
4. **Try GitHub first** - Most reliable sources
5. **Use API-based job sites** - RemoteOK, Remotive, WeWorkRemotely don't need proxies

---

## 📈 Upgrade Path

### For Production Use
Consider these paid proxy services:
- **BrightData** (formerly Luminati) - Enterprise-grade
- **Oxylabs** - High success rate
- **ScraperAPI** - Easy integration
- **Smartproxy** - Good balance of price/quality

### Integration
Paid proxies can be added manually in the Proxy Manager:
1. Get proxy credentials from provider
2. Click "Add Proxy" in GUI
3. Enter proxy URL with authentication
4. Format: `http://username:password@proxy.example.com:8080`

---

**Last Updated**: December 9, 2025
**Total Proxy Sources**: 8 (5 GitHub + 3 Web Scrapers)
**Estimated Proxies Available**: 10,000+ across all sources
