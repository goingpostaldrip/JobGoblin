# 🔗 Proxy Setup Guide

## What are Proxies?
Proxies act as intermediaries that hide your IP address and can help bypass rate limiting and bot detection. Using rotating proxies allows the scraper to bypass website blocks.

## Why Use Proxies?
- ✅ Bypass CAPTCHA challenges
- ✅ Avoid IP bans and rate limiting
- ✅ Rotate between different IPs
- ✅ Appear as legitimate requests

## How to Get Proxies

### Free Proxy Lists (⚠️ Lower Quality)
1. **Proxy List Download**: https://www.proxy-list.download/
2. **Free Proxy Lists**: https://www.freeproxylists.net/
3. **US Proxy**: https://www.us-proxy.org/
4. **Free Proxy List**: https://free-proxy-list.com/

**Tips for free proxies:**
- Usually work for a few hours before failing
- Often slow or unreliable
- Good for testing but not production
- Many are already in use by others

### Paid Proxy Services (✅ Recommended)
Paid services provide more reliable, faster proxies:

1. **Bright Data (formerly Luminati)**
   - Best for residential proxies
   - Excellent for scraping
   - Website: https://brightdata.com/

2. **Oxylabs**
   - High-quality residential proxies
   - Great success rate
   - Website: https://oxylabs.io/

3. **Smartproxy**
   - Affordable residential proxies
   - Good performance
   - Website: https://smartproxy.com/

4. **Residential Proxies**
   - IPQualityScore, Storm Proxies, etc.
   - Best for maximum success

## How to Add a Proxy

### In the GUI:
1. Click the **"🔗 Proxy Manager"** tab
2. Enter proxy URL: `http://123.45.67.89:8080`
3. Select type: http/socks5
4. (Optional) Add username and password
5. Click **"Add Proxy"**
6. Click **"Test Proxy"** to verify it works

### Proxy URL Formats:
```
http://123.45.67.89:8080
socks5://123.45.67.89:1080
http://username:password@123.45.67.89:8080
```

## Testing Your Proxy

1. Add the proxy
2. Click **"Test Proxy"**
3. If it says ✓ WORKING, you're ready to scrape!
4. If it says ✗ FAILED, try a different proxy

## Using Proxies in Scraping

Once you've added proxies to the app:
1. Go to **"🟢 Job Scraper"** tab
2. Configure your search (keywords, locations, engines)
3. Click **"Start Scraping"**
4. The app automatically rotates through your proxies
5. Each request uses a different proxy

## Troubleshooting

### "CAPTCHA challenge detected"
- Try adding more proxies
- Use paid proxies for better success
- Wait a few hours before retrying

### Proxy still not working
- Check if the IP is accessible
- Verify username/password if using auth
- Try a different proxy service
- Check if the proxy is already banned

### Slow scraping with proxies
- Proxies can reduce speed, this is normal
- Free proxies are much slower
- Use paid proxies for better performance

## Best Practices

1. **Use Multiple Proxies** - Add 5-10 proxies for rotation
2. **Test Before Scraping** - Always test proxies first
3. **Rotate Regularly** - Change proxies if one gets blocked
4. **Use Paid for Production** - Free proxies fail frequently
5. **Monitor Success Rate** - Check results for blocks
6. **Take Breaks** - Add delays between requests
7. **Respect Robots.txt** - Don't overload target sites

## Example Workflow

```
1. Sign up for Smartproxy or similar service
2. Get 5 residential proxy URLs
3. Open "Proxy Manager" tab in app
4. Add all 5 proxies (test each one)
5. Go to Job Scraper
6. Run your scrape
7. App rotates through all 5 proxies automatically
8. Get results successfully!
```

## Need More Help?

- **Proxy Manager Issues**: Check proxy format and URL
- **Scraping Still Failing**: Try different proxy service
- **Performance Issues**: Use paid proxies instead of free
- **IP Still Banned**: Wait 24-48 hours before retrying

---

**Remember**: Proxies are most effective when used with responsible scraping practices!
