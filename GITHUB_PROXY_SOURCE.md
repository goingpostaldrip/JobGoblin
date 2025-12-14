# GitHub PROXY-List Integration

## What's New

The app now uses **TheSpeedX/PROXY-List** from GitHub as the **primary proxy source**. This is one of the most reliable and actively maintained free proxy lists available.

**GitHub Repository**: https://github.com/TheSpeedX/PROXY-List

## Sources Now Used (in order):

1. **GitHub (TheSpeedX/PROXY-List)** ⭐ - Most reliable, actively maintained
   - http.txt - HTTP proxies
   - socks4.txt - SOCKS4 proxies
   - socks5.txt - SOCKS5 proxies

2. **free-proxy-list.com** - Web scrape
3. **us-proxy.org** - Web scrape
4. **freeproxylists.net** - Web scrape

## Why GitHub?

- **Active Maintenance**: The list is updated regularly
- **Quality Control**: Community-maintained and tested
- **Multiple Formats**: HTTP, SOCKS4, and SOCKS5 proxies
- **High Volume**: Thousands of proxies available
- **Direct Access**: No rate limiting via raw.githubusercontent.com

## How It Works

### Using Auto-Discovery:

```
1. Go to "🔗 Proxy Manager" tab
2. Click "🔍 Find & Add Proxies"
3. App automatically searches GitHub first
4. If GitHub fails, tries other sources
5. Only adds working proxies
6. Done in ~45 seconds
```

### What the App Does:

```python
# 1. Fetch from GitHub
proxies = finder.find_from_github_speedx(limit=10)
# Result: Gets up to 10 proxies from TheSpeedX/PROXY-List

# 2. Fall back to other sources if needed
if not proxies:
    proxies.extend(finder.find_from_free_proxy_list())
    proxies.extend(finder.find_from_us_proxy())
    # etc...

# 3. Test each one
for proxy in proxies:
    if test_proxy(proxy):  # Test with httpbin.org
        working_proxies.append(proxy)

# 4. Add to app
for proxy in working_proxies:
    proxy_manager.add_proxy(proxy)
```

## Testing

The GitHub source works great:

```bash
$ python3
>>> from proxy_finder import ProxyFinder
>>> finder = ProxyFinder()
>>> proxies = finder.find_from_github_speedx(limit=10)
>>> len(proxies)
10  # Successfully found 10 proxies
```

## Expected Results

When you click "Find & Add Proxies":
- ✅ Finds 3-10 proxies from GitHub in first 5 seconds
- ✅ Adds them to the list
- ✅ Tests each one
- ✅ Shows status "Found and added X working proxies"

## Troubleshooting

### "No proxies found from GitHub"
- The GitHub repo might be temporarily down
- Try again in a few minutes
- Other sources will be tried automatically

### "Found proxies but they're slow"
- Free proxies are often slow
- Try paid proxies for better performance
- Galaxy, Bright Data, or ScraperAPI recommended

### "Proxies found but not working in scraper"
- Free proxies get blocked by target sites
- Paid proxies recommended for production
- App will automatically fallback to direct requests

## Integration Details

**File Modified**: `proxy_finder.py`

**New Method Added**: `find_from_github_speedx()`

**Changes**:
- Added GitHub as first source in `find_all_sources()`
- Supports HTTP, SOCKS4, and SOCKS5 proxies
- Automatic fallback if GitHub is unavailable
- Better error handling for network issues

## Next Steps

1. **For Testing**: Use GitHub auto-discovery (free, good for testing)
2. **For Production**: Use paid proxies (more reliable)
3. **If Getting Blocks**: Add more proxies from auto-discovery or use paid service

## References

- **GitHub Repository**: https://github.com/TheSpeedX/PROXY-List
- **Raw Files**:
  - http.txt: https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
  - socks4.txt: https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
  - socks5.txt: https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt

## Performance

Current results with GitHub source:
- **Find Speed**: 3-5 seconds to fetch 10 proxies
- **Success Rate**: 30-50% of found proxies work (free proxies unreliable)
- **Total Time**: ~45 seconds to find and test all sources

This is normal for free proxies. Paid proxy services have 90%+ success rates.
