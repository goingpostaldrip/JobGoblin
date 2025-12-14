import argparse
import json
import time
import os
import sys
import math
from typing import List
from dotenv import load_dotenv
from search_engines import ENGINE_FUNCS
from site_indeed import indeed_search
from site_greenhouse import greenhouse_search
from site_lever import lever_search
from site_simplyhired import simplyhired_search
from normalize import normalize_record, is_relevant
from email_extractor import extract_from_job_results, filter_and_dedupe_emails
from email_manager import EmailManager
from email_sender import EmailSender
from enrichment_pipeline import JobEnrichment, filter_by_enrichment_score, sort_by_enrichment, export_enriched_jobs

load_dotenv()

def expand_queries(keywords: List[str], locations: List[str]) -> List[str]:
    out = []
    for kw in keywords:
        kw = kw.strip()
        if not kw:
            continue
        if locations:
            for loc in locations:
                loc = loc.strip()
                if not loc:
                    continue
                out.append(f"{kw} {loc}")
        else:
            out.append(kw)
    return out

def dedupe(existing: List[dict], new: List[dict]) -> List[dict]:
    seen = {r.get("url"): True for r in existing}
    merged = existing[:]
    for r in new:
        u = r.get("url")
        if u and u not in seen:
            merged.append(r)
            seen[u] = True
    return merged

def main():
    ap = argparse.ArgumentParser(description="JOB SCRAPER ULTIMATE - broad search engine job discovery")
    ap.add_argument("--keywords", required=True, help="Comma-separated keyword phrases")
    ap.add_argument("--locations", default="", help="Comma-separated location phrases")
    ap.add_argument("--engines", default="duckduckgo", help="Comma-separated engine list (duckduckgo,google_cse,bing,serpapi,indeed,linkedin)")
    ap.add_argument("--max-per-query", type=int, default=20, help="Max results per query per engine")
    ap.add_argument("--out", default="web_jobs_ultimate.json", help="Output JSON path")
    ap.add_argument("--txt-out", default="", help="Optional TXT summary path (defaults to output/web_jobs_ultimate.txt)")
    ap.add_argument("--append", action="store_true", help="Append/dedupe into existing output file")
    ap.add_argument("--csv-out", default="", help="Optional CSV export path")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--throttle", type=float, default=1.2, help="Seconds sleep between queries per engine")
    ap.add_argument("--relevance-threshold", type=float, default=1.0, help="Score threshold for relevance filter")
    ap.add_argument("--no-auto-serpapi", action="store_true", help="Disable automatic SerpAPI fallback when zero results")
    ap.add_argument("--email-to", default="", help="Comma-separated recipients (uses SENDGRID_API_KEY)")
    ap.add_argument("--email-top", type=int, default=10, help="Top N results to email")
    ap.add_argument("--email-subject", default="Job Scraper Ultimate Results", help="Email subject line")
    ap.add_argument("--extract-emails", action="store_true", help="Extract contact emails from found job postings")
    ap.add_argument("--emails-csv", default="", help="Output path for extracted emails CSV (defaults to output/found_emails.csv)")
    ap.add_argument("--send-emails", action="store_true", help="Send emails to extracted contacts (respects 50/day limit)")
    ap.add_argument("--email-timeout", type=int, default=10, help="Timeout in seconds for email extraction from websites")
    ap.add_argument("--enrich", action="store_true", help="Enrich results with emails and company info (enabled by default)")
    ap.add_argument("--no-enrich", action="store_true", help="Disable enrichment pipeline")
    args = ap.parse_args()

    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    locations = [l.strip() for l in args.locations.split(',') if l.strip()]
    engines = [e.strip() for e in args.engines.split(',') if e.strip()]

    queries = expand_queries(keywords, locations)
    if args.verbose:
        print(f"Expanded {len(keywords)} keywords + {len(locations)} locations -> {len(queries)} queries")

    existing = []
    if args.append and os.path.exists(args.out):
        try:
            with open(args.out, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            if args.verbose:
                print(f"Loaded {len(existing)} existing records from {args.out}")
        except Exception as e:
            print("Failed loading existing output", e)
            existing = []

    all_new = []

    # Separate handling: web search engines (query string) vs site engines (kw+loc)
    WEB_ENGINES = set(["duckduckgo", "google_cse", "bing", "serpapi", "linkedin", "glassdoor", "ziprecruiter"])
    SITE_ENGINES = set(["indeed", "greenhouse", "lever", "simplyhired"])

    # Web engines use combined queries
    for q_idx, query in enumerate(queries, 1):
        for eng in engines:
            if eng not in WEB_ENGINES:
                continue
            # Special site-filtered engines via SerpAPI
            modified_query = query
            if eng in ("linkedin", "glassdoor", "ziprecruiter"):
                site_map = {
                    "linkedin": "site:linkedin.com/jobs ",
                    "glassdoor": "site:glassdoor.com/Job ",
                    "ziprecruiter": "site:ziprecruiter.com/jobs "
                }
                if "serpapi" in ENGINE_FUNCS:
                    fn = ENGINE_FUNCS.get("serpapi")
                    modified_query = site_map[eng] + query
                else:
                    if args.verbose:
                        print(f"{eng} requires SerpAPI for site-filtered search; skipping")
                    continue
            else:
                fn = ENGINE_FUNCS.get(eng)
            if not fn:
                if args.verbose:
                    print(f"Unknown web engine {eng}; skipping")
                continue
            if args.verbose:
                print(f"[{q_idx}/{len(queries)}] Engine {eng} querying: {modified_query}")
            results = fn(modified_query, max_results=args.max_per_query, verbose=args.verbose)
            filtered = [normalize_record(r) for r in results if is_relevant(r.get("title", ""), r.get("snippet", ""), keywords, args.relevance_threshold)]
            if args.verbose:
                print(f"Engine {eng} raw {len(results)} -> relevant {len(filtered)}")
            all_new.extend(filtered)
            time.sleep(args.throttle)

    # Site engines iterate keyword x location pairs
    for eng in engines:
        if eng not in SITE_ENGINES:
            continue
        if args.verbose:
            print(f"[site] Engine {eng} over {len(keywords)} keywords x {max(1,len(locations))} locations")
        for kw in keywords:
            if locations:
                locs = locations
            else:
                locs = [""]
            for loc in locs:
                if args.verbose:
                    print(f"[site] {eng} kw='{kw}' loc='{loc}'")
                if eng == "indeed":
                    results = indeed_search(kw, loc, max_results=args.max_per_query, verbose=args.verbose)
                elif eng == "greenhouse":
                    results = greenhouse_search(kw, loc, max_results=args.max_per_query, verbose=args.verbose)
                elif eng == "lever":
                    results = lever_search(kw, loc, max_results=args.max_per_query, verbose=args.verbose)
                elif eng == "simplyhired":
                    results = simplyhired_search(kw, loc, max_results=args.max_per_query, verbose=args.verbose)
                else:
                    results = []
                filtered = [normalize_record(r) for r in results if is_relevant(r.get("title", ""), r.get("snippet", ""), keywords, args.relevance_threshold)]
                if args.verbose:
                    print(f"[site] {eng} raw {len(results)} -> relevant {len(filtered)}")
                all_new.extend(filtered)
                time.sleep(args.throttle)

    merged = dedupe(existing, all_new)
    if args.verbose:
        print(f"Total new relevant {len(all_new)}; merged unique {len(merged)}")

    # Auto SerpAPI fallback if nothing found and key present
    if not merged and not args.no_auto_serpapi:
        serpapi_key = os.getenv("SERPAPI_KEY")
        if serpapi_key:
            if "serpapi" not in engines:
                if args.verbose:
                    print("No results; auto SerpAPI fallback engaged.")
                for q_idx, query in enumerate(queries, 1):
                    fn = ENGINE_FUNCS.get("serpapi")
                    if not fn:
                        continue
                    if args.verbose:
                        print(f"[fallback {q_idx}/{len(queries)}] serpapi querying: {query}")
                    results = fn(query, max_results=args.max_per_query, verbose=args.verbose)
                    filtered = [normalize_record(r) for r in results if is_relevant(r.get("title", ""), r.get("snippet", ""))]
                    merged = dedupe(merged, filtered)
                    time.sleep(args.throttle)
            else:
                if args.verbose:
                    print("SerpAPI already in engine list; no extra fallback.")
        else:
            if args.verbose:
                print("SerpAPI key missing; fallback skipped.")

    # ===== ENRICHMENT PIPELINE =====
    # Enhance job listings with emails, company info, and validation
    if merged and not args.no_enrich:
        if args.verbose:
            print(f"\n[enrichment] Starting enrichment pipeline for {len(merged)} jobs...")
        
        enricher = JobEnrichment(verbose=args.verbose)
        enriched = enricher.enrich_jobs(merged)
        
        # Sort by enrichment score (highest first)
        enriched = sort_by_enrichment(enriched, reverse=True)
        
        if args.verbose:
            avg_score = sum(j.get("enrichment_score", 0) for j in enriched) / len(enriched) if enriched else 0
            print(f"[enrichment] Complete. Average enrichment score: {avg_score:.1f}/12.0")
        
        merged = enriched

    try:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2)
    except Exception as e:
        print("Error writing output", e)
        sys.exit(1)

    # Optional CSV export via flag
    csv_out = args.csv_out.strip()
    if csv_out:
        import csv
        try:
            with open(csv_out, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerow(["title","url","engine","query","snippet"])
                for r in merged:
                    w.writerow([r.get('title',''), r.get('url',''), r.get('engine',''), r.get('query',''), r.get('snippet','')])
        except Exception as e:
            print("Failed writing CSV", e)

    # Prepare TXT summary output
    txt_out = args.txt_out.strip()
    if not txt_out:
        os.makedirs('output', exist_ok=True)
        txt_out = os.path.join('output', 'web_jobs_ultimate.txt')
    lines = []
    for r in merged:
        lines.append(f"{r.get('title','').strip()} | {r.get('url','')} | {r.get('engine','')} | {r.get('query','')}")
    try:
        with open(txt_out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print("Failed writing TXT summary", e)
        # Continue; JSON already written

    msg = f"Wrote {len(merged)} records to {args.out} and summary {txt_out}"
    if csv_out:
        msg += f"; CSV {csv_out}"
    print(msg)

    # Email extraction from found job postings
    extracted_emails = {}
    if args.extract_emails and merged:
        print(f"\n[EMAIL EXTRACTION] Extracting emails from {len(merged)} job postings...")
        
        try:
            company_emails = extract_from_job_results(merged, verbose=args.verbose)
            extracted_emails = filter_and_dedupe_emails(company_emails)
            
            if args.verbose:
                print(f"[EMAIL EXTRACTION] Found {len(extracted_emails)} unique emails from {len(company_emails)} domains")
            
            # Export to CSV
            emails_csv = args.emails_csv.strip()
            if not emails_csv:
                os.makedirs('output', exist_ok=True)
                emails_csv = os.path.join('output', 'found_emails.csv')
            
            email_mgr = EmailManager(os.path.dirname(emails_csv) or 'output', verbose=args.verbose)
            csv_path = email_mgr.export_emails_to_csv(extracted_emails, emails_csv)
            print(f"[EMAIL EXTRACTION] Exported {len(extracted_emails)} emails to {csv_path}")
            
        except Exception as e:
            print(f"[EMAIL EXTRACTION] Error extracting emails: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
    
    # Email sending to extracted contacts
    if args.send_emails and extracted_emails:
        print(f"\n[EMAIL SENDING] Preparing to send emails to {len(extracted_emails)} contacts...")
        
        try:
            emails_csv = args.emails_csv.strip()
            if not emails_csv:
                emails_csv = os.path.join('output', 'found_emails.csv')
            
            sender = EmailSender(verbose=args.verbose)
            stats = sender.send_emails_from_csv(
                emails_csv,
                subject="Potential Job Opportunity",
                limit_per_run=50
            )
            
            daily_stats = sender.get_daily_stats()
            print(f"[EMAIL SENDING] Sent: {stats['sent']}, Failed: {stats['failed']}, Skipped: {stats['skipped']}")
            print(f"[EMAIL SENDING] Daily stats: {daily_stats['emails_sent_today']}/{daily_stats['daily_limit']} emails sent today")
            
        except Exception as e:
            print(f"[EMAIL SENDING] Error sending emails: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()

    # Optional email of top N results via SendGrid
    recipients = [x.strip() for x in args.email_to.split(',') if x.strip()]
    if recipients:
        sg_key = os.getenv("SENDGRID_API_KEY")
        if not sg_key:
            print("SENDGRID_API_KEY not set; email skipped")
        else:
            try:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import Mail
                top = merged[: max(1, args.email_top)]
                lines = [f"{r.get('title','')}\n{r.get('url','')}\n{r.get('engine','')} | {r.get('query','')}\n" for r in top]
                body = "\n\n".join(lines) if top else "No results."
                message = Mail(
                    from_email=os.getenv("SMTP_USER", "noreply@example.com"),
                    to_emails=recipients,
                    subject=args.email_subject,
                    plain_text_content=body
                )
                sg = SendGridAPIClient(sg_key)
                resp = sg.send(message)
                if args.verbose:
                    print(f"Email sent status: {resp.status_code}")
            except Exception as e:
                print("Email send failed:", e)

if __name__ == "__main__":
    main()
