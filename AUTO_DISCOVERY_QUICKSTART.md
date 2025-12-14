# 🚀 Auto-Discovery Proxy - 2 Minute Setup

## TL;DR - Just Do This:

1. Open app
2. Click **"🔗 Proxy Manager"** tab
3. Click **"🔍 Find & Add Proxies"** button
4. Wait ~45 seconds
5. Go to **Job Scraper** and scrape!

## The Long Version

### Step 1: Open Proxy Manager Tab
- Look at top of app where it says 🔗 Proxy Manager
- Click it
- You'll see auto-discovery section at the top

### Step 2: Configure Auto-Discovery
- See a number field that says "5"
- You can change this (1-20 proxies)
- 5 is good for starting
- 10-15 for heavy scraping

### Step 3: Click Find & Add Proxies
- Big button that says "🔍 Find & Add Proxies"
- Click it
- Status will show: "🔍 Searching for proxies..."

### Step 4: Wait for Results
- Takes 30-60 seconds
- App searches multiple proxy sources
- Tests each one to ensure it works
- Only adds working proxies

### Step 5: See Results
- Proxies appear in list below
- Shows like: ✓ [0] http://123.45.67.89:8080
- The ✓ means working!

### Step 6: Start Scraping!
- Go to "🟢 Job Scraper" tab
- Set keywords and locations
- Click "Start Scraping"
- Proxies rotate automatically!

## What's Happening Behind the Scenes

The app is:
1. ✓ Searching 4 major proxy lists simultaneously
2. ✓ Testing each proxy for reliability
3. ✓ Validating IP addresses
4. ✓ Checking actual connectivity
5. ✓ Removing duplicates
6. ✓ Adding only working ones to your list

## Status Messages Explained

| Status | Meaning | What to Do |
|--------|---------|-----------|
| 🔍 Searching... | Currently finding proxies | Wait 30-60 seconds |
| ✓ Found X proxies! | Success! | Go scrape now |
| ❌ No proxies found | All tested failed | Try again in 5 mins |
| ❌ Error: timeout | Network issue | Check internet, retry |

## Customizing Count

**Want 3 proxies?**
- Change "5" to "3"
- Takes ~20 seconds
- Faster but less rotation

**Want 15 proxies?**
- Change "5" to "15"
- Takes ~60 seconds
- Better for heavy scraping

**Want 1 for testing?**
- Change "5" to "1"
- Takes ~10 seconds
- Good for quick test

## What If It Fails?

### "No working proxies found"
```
Try again after 5 minutes
(Free proxies are unreliable)
```

### "Still getting CAPTCHA after proxies added"
```
Option 1: Click discovery again (fresh IPs)
Option 2: Increase count to 15
Option 3: Try paid proxies (more reliable)
```

### "One proxy stopped working"
```
Click "Find & Add Proxies" again
Adds fresh working proxies
Mix with existing ones
```

## Free vs Paid - When to Switch

### Free Proxies (Auto-Discovery) - Good For:
- Testing the app
- Light scraping (1-2 hours)
- Learning how proxies work
- Free trial before investing

### Paid Proxies (Manual Add) - Better For:
- Production scraping
- Long sessions (6+ hours)
- High success rate needed
- When free ones die

### Paid Proxy Cost:
- Smartproxy: $5-20/month
- Oxylabs: $8-50/month
- Bright Data: $6+/month
- Often cheaper than expected!

## Advanced: Mix Free + Paid

Want best of both worlds?
1. Click "Find & Add Proxies" (free ones)
2. Manually add 2-3 paid proxy URLs
3. Run scraper with all of them
4. Free ones for bulk, paid ones as backup

## Real Usage Example

```
Monday 9 AM:
1. Click "Find & Add Proxies"
2. Wait 45 seconds
3. Get 5 working proxies
4. Start scraping Python jobs

Monday 12 PM:
5. Some free proxies died
6. Results slower/fewer
7. Click "Find & Add Proxies" again
8. Refresh with fresh batch
9. Continue scraping

Monday 5 PM:
10. Still using same proxies
11. Getting blocked occasionally
12. Consider switching to paid
13. Sign up Smartproxy ($5)
14. Add 2 paid proxy URLs
15. Mix with free ones
16. Better success rate!

Next Day:
17. Use paid + free mix
18. More stable results
19. 10x better than free alone
```

## Troubleshooting Checklist

- [ ] Click button - wait full 45 seconds
- [ ] Check proxies actually appear in list
- [ ] Verify they start with "✓" (working)
- [ ] Go to Job Scraper tab
- [ ] Try scraping with proxies
- [ ] If blocked, add more proxies (run discovery again)
- [ ] If still blocked, consider paid proxies

## FAQ

**Q: Why does discovery take 45 seconds?**
A: It's testing 20+ proxies. Each test takes 2-5 seconds.

**Q: Can I add proxies manually too?**
A: Yes! Use "Add New Proxy" section for manual entry.

**Q: What if I want different proxy count next time?**
A: Change the number, click button again!

**Q: Do proxies expire?**
A: Yes, free proxies die constantly. Run discovery again.

**Q: Can I use the app without proxies?**
A: Yes, but you'll hit DuckDuckGo blocks quickly.

**Q: Will paid proxies work with this?**
A: Yes! Manually add paid proxy URLs, they rotate automatically.

## Next Steps

1. **Try discovery now** - Click button, wait 45 seconds
2. **Test scraping** - Go to Job Scraper, try a search
3. **If blocked** - Run discovery again for fresh IPs
4. **If working well** - Keep using free proxies!
5. **If unreliable** - Consider cheap paid option ($5)

## You're All Set! 🎉

Auto-discovery makes proxy setup instant and painless. No more:
- Opening browsers
- Searching websites
- Copying/pasting
- Testing manually

Just click button → wait → scrape! ✨

---

**Pro Tips:**
- Run discovery every 2-3 hours if scraping long
- Keep 10-15 proxies for best rotation
- Free proxies = good for testing
- Paid proxies = good for production
- Mix both for maximum reliability

Happy scraping! 🚀
