"""
Check daily email sending status and history
"""
import os
import json
from datetime import datetime
from email_manager import EmailManager

def format_timestamp(iso_string):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %I:%M:%S %p")
    except:
        return iso_string

def main():
    print("=" * 60)
    print("JOB SCRAPER ULTIMATE - Email Status Check")
    print("=" * 60)
    print()
    
    # Get daily stats
    email_mgr = EmailManager(output_dir="output", verbose=False)
    stats = email_mgr.get_daily_stats()
    
    print("📊 DAILY STATUS:")
    print(f"  Emails sent today: {stats['emails_sent_today']}")
    print(f"  Daily limit: {stats['daily_limit']}")
    print(f"  Remaining: {stats['remaining']}")
    print(f"  Success: {stats['success_count']}")
    print(f"  Failed: {stats['failed_count']}")
    print()
    
    # Show today's sends
    sent_today_file = os.path.join("output", ".emails_sent_today.json")
    if os.path.exists(sent_today_file):
        try:
            with open(sent_today_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print("📧 TODAY'S EMAILS:")
            emails = data.get('emails_sent', [])
            
            if emails:
                for i, email in enumerate(emails[-10:], 1):  # Show last 10
                    timestamp = format_timestamp(email.get('timestamp', ''))
                    recipient = email.get('recipient_email', 'N/A')
                    status = email.get('status', 'unknown')
                    status_icon = "✅" if status == "success" else "❌"
                    print(f"  {i}. {status_icon} {recipient} - {timestamp}")
                
                if len(emails) > 10:
                    print(f"  ... and {len(emails) - 10} more")
            else:
                print("  No emails sent yet today")
                
        except Exception as e:
            print(f"  Error reading today's file: {e}")
    else:
        print("📧 TODAY'S EMAILS:")
        print("  No emails sent yet today")
    
    print()
    
    # Show email history summary
    history_file = os.path.join("output", "email_send_history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            total = len(history)
            success = len([e for e in history if e.get('status') == 'success'])
            failed = total - success
            
            print("📈 OVERALL HISTORY:")
            print(f"  Total emails sent: {total}")
            print(f"  Successful: {success}")
            print(f"  Failed: {failed}")
            
            if total > 0:
                print()
                print("  Last 5 emails:")
                for i, email in enumerate(history[-5:], 1):
                    timestamp = format_timestamp(email.get('timestamp', ''))
                    recipient = email.get('recipient_email', 'N/A')
                    status = email.get('status', 'unknown')
                    status_icon = "✅" if status == "success" else "❌"
                    print(f"    {i}. {status_icon} {recipient} - {timestamp}")
        except Exception as e:
            print(f"  Error reading history: {e}")
    else:
        print("📈 OVERALL HISTORY:")
        print("  No email history found")
    
    print()
    
    # Check for extracted emails
    emails_csv = os.path.join("output", "found_emails.csv")
    if os.path.exists(emails_csv):
        try:
            import csv
            with open(emails_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                emails = list(reader)
            
            print("📋 EXTRACTED EMAILS CSV:")
            print(f"  File: {emails_csv}")
            print(f"  Total emails in CSV: {len(emails)}")
            print(f"  Ready to send: {min(len(emails), stats['remaining'])}")
        except Exception as e:
            print(f"  Error reading CSV: {e}")
    else:
        print("📋 EXTRACTED EMAILS CSV:")
        print("  No emails CSV found")
        print("  Run with --extract-emails to generate")
    
    print()
    print("=" * 60)
    
    # Give recommendations
    if stats['remaining'] > 0:
        print("💡 RECOMMENDATIONS:")
        if os.path.exists(emails_csv):
            print(f"  You can send {stats['remaining']} more emails today")
            print(f"  Run: python send_emails.py --csv output/found_emails.csv --limit {stats['remaining']}")
        else:
            print("  Run job scraper with --extract-emails to find contact emails")
    else:
        print("💡 RECOMMENDATIONS:")
        print("  Daily limit reached. Try again tomorrow!")
        print("  Limit will reset at midnight")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
