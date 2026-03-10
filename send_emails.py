"""
Standalone email sender script - sends emails from CSV without scraping
Use this to send emails from a previously extracted emails CSV file
"""
import argparse
import os
import sys
from dotenv import load_dotenv
from email_sender import EmailSender

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Send emails from CSV file (max 50/day)")
    parser.add_argument("--csv", required=True, help="Path to CSV file with emails")
    parser.add_argument("--subject", default="Potential Opportunity", help="Email subject line")
    parser.add_argument("--message", default="", help="Email message template (optional)")
    parser.add_argument("--limit", type=int, default=50, help="Max emails to send (default 50)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be sent without actually sending")
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    
    args = parser.parse_args()
    
    # Check if CSV exists
    if not os.path.exists(args.csv):
        print(f"Error: CSV file not found: {args.csv}")
        sys.exit(1)
    
    # Check email backend configuration
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    smtp_host = os.getenv("SMTP_HOST")
    
    if not sendgrid_key and not smtp_host:
        print("Error: No email backend configured!")
        print("")
        print("Please set one of the following:")
        print("")
        print("Option 1: SendGrid")
        print("  export SENDGRID_API_KEY='SG.xxxxxxxxxxxxx'")
        print("")
        print("Option 2: SMTP (Gmail, etc)")
        print("  export SMTP_HOST='smtp.gmail.com'")
        print("  export SMTP_PORT='587'")
        print("  export SMTP_USER='your@gmail.com'")
        print("  export SMTP_PASSWORD='app_password'")
        print("")
        sys.exit(1)
    
    # Create sender
    sender = EmailSender(verbose=args.verbose)
    
    # Get daily stats first
    stats = sender.get_daily_stats()
    print(f"Daily Email Status: {stats['emails_sent_today']}/{stats['daily_limit']} sent today")
    print(f"Remaining today: {stats['remaining']}")
    print("")
    
    if stats['remaining'] <= 0:
        print("Daily limit reached. Try again tomorrow.")
        sys.exit(0)
    
    if args.dry_run:
        print("[DRY RUN MODE] No emails will actually be sent")
        print("")
    
    # Send emails
    print(f"Sending emails from {args.csv}...")
    print(f"Subject: {args.subject}")
    print(f"Limit: {min(args.limit, stats['remaining'])}")
    print("")
    
    result = sender.send_emails_from_csv(
        csv_file=args.csv,
        subject=args.subject,
        message_template=args.message if args.message else None,
        dry_run=args.dry_run,
        limit_per_run=args.limit
    )
    
    print("")
    print("=" * 50)
    print("Email Campaign Results:")
    print(f"  Sent: {result['sent']}")
    print(f"  Failed: {result['failed']}")
    print(f"  Skipped: {result['skipped']}")
    print("=" * 50)
    
    # Show updated stats
    stats = sender.get_daily_stats()
    print(f"Daily Status: {stats['emails_sent_today']}/{stats['daily_limit']} emails sent today")
    print(f"Remaining: {stats['remaining']}")
    
    if result['failed'] > 0:
        print("")
        print("Check output/email_send_history.json for error details")

if __name__ == "__main__":
    main()
