"""
Email sender - handles bulk email sending with 50/day limit and scheduling
"""
import os
import time
from typing import List, Dict, Tuple
from email_manager import EmailManager


def _load_env_file(env_path: str = ".env") -> None:
    """Load .env key/value pairs into os.environ (lightweight dotenv)."""
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()
    except Exception:
        # Fail silently; caller can still rely on existing env vars
        pass

class EmailSender:
    """Sends emails respecting daily 50-email limit"""
    
    def __init__(self, from_email: str = "", email_manager: EmailManager = None, verbose: bool = False):
        # Always refresh env vars from .env so latest GUI settings are used
        _load_env_file()

        self.from_email = from_email or os.getenv("SMTP_USER", "noreply@leadfinder.com")
        self.email_manager = email_manager or EmailManager(verbose=verbose)
        self.verbose = verbose
        self.sendgrid_key = os.getenv("SENDGRID_API_KEY", "")
        self.smtp_enabled = False

        # SMTP-only: always pick SMTP when available, ignore SendGrid
        smtp_host = os.getenv("SMTP_HOST")
        if smtp_host:
            self.backend = "smtp"
            self.smtp_config = {
                'host': smtp_host,
                'port': int(os.getenv("SMTP_PORT", "587")),
                'user': os.getenv("SMTP_USER", ""),
                'password': os.getenv("SMTP_PASSWORD", "")
            }
            if verbose:
                print(f"[email_sender] Using SMTP backend ({self.smtp_config['host']})")
        else:
            self.backend = None
            print("[email_sender] WARNING: No SMTP credentials configured (SMTP_HOST missing)")
    
    def send_emails_from_csv(self, csv_file: str, subject: str = "Job Lead Information", 
                            message_template: str = None, dry_run: bool = False, 
                            limit_per_run: int = 50) -> Dict[str, int]:
        """
        Read emails from CSV and send to each one.
        Respects daily 50-email limit.
        """
        if not self.backend:
            print("[email_sender] No email backend configured. Set SENDGRID_API_KEY or SMTP_HOST env vars.")
            return {'sent': 0, 'failed': 0, 'skipped': 0}
        
        # Load emails from CSV
        try:
            emails_to_send = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('email', '').strip()
                    if email:
                        emails_to_send.append({
                            'email': email,
                            'domains': row.get('domains', ''),
                            'job_titles': row.get('job_titles', '')
                        })
        except Exception as e:
            print(f"[email_sender] Error reading CSV: {e}")
            return {'sent': 0, 'failed': 0, 'skipped': 0}
        
        # Check daily limit
        remaining, sent_today = self.email_manager.get_emails_to_send(limit=limit_per_run)
        
        if remaining <= 0:
            print(f"[email_sender] Daily limit reached ({limit_per_run} emails)")
            return {'sent': 0, 'failed': 0, 'skipped': len(emails_to_send)}
        
        # Limit emails to send
        emails_to_send = emails_to_send[:remaining]
        
        if self.verbose:
            print(f"[email_sender] Will send {len(emails_to_send)} emails (daily limit: {limit_per_run})")
        
        # Send emails
        stats = {'sent': 0, 'failed': 0, 'skipped': 0}
        
        for idx, email_data in enumerate(emails_to_send, 1):
            recipient = email_data['email']
            
            if dry_run:
                print(f"[DRY RUN] Would send email to {recipient}")
                stats['sent'] += 1
                continue
            
            try:
                # Format message
                body = self._format_message(email_data, message_template)
                
                # Send via appropriate backend
                if self.backend == "sendgrid":
                    success = self._send_via_sendgrid(recipient, subject, body)
                elif self.backend == "smtp":
                    success = self._send_via_smtp(recipient, subject, body)
                else:
                    success = False
                
                if success:
                    self.email_manager.mark_email_sent(recipient, recipient, subject, "success")
                    stats['sent'] += 1
                    if self.verbose:
                        print(f"[{idx}/{len(emails_to_send)}] Sent to {recipient}")
                else:
                    self.email_manager.mark_email_sent(recipient, recipient, subject, "failed")
                    stats['failed'] += 1
                    if self.verbose:
                        print(f"[{idx}/{len(emails_to_send)}] Failed to send to {recipient}")
                
                # Rate limiting - space out emails
                if idx < len(emails_to_send):
                    time.sleep(1)  # 1 second between emails
            
            except Exception as e:
                self.email_manager.mark_email_sent(recipient, recipient, subject, f"error: {str(e)}")
                stats['failed'] += 1
                if self.verbose:
                    print(f"[{idx}/{len(emails_to_send)}] Error sending to {recipient}: {e}")
        
        return stats
    
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Send a single email to a recipient.
        Returns True if successful, False otherwise.
        """
        if not self.backend:
            if self.verbose:
                print("[email_sender] No email backend configured.")
            return False
        
        try:
            if self.backend == "sendgrid":
                success = self._send_via_sendgrid(recipient, subject, body)
            elif self.backend == "smtp":
                success = self._send_via_smtp(recipient, subject, body)
            else:
                success = False
            
            if success and self.verbose:
                print(f"[email_sender] Successfully sent email to {recipient}")
            elif not success and self.verbose:
                print(f"[email_sender] Failed to send email to {recipient}")
            
            return success
        
        except Exception as e:
            if self.verbose:
                print(f"[email_sender] Error sending email to {recipient}: {e}")
            return False
    
    def send_to_list(self, recipient_list: List[str], subject: str = "Job Lead Information",
                    message_template: str = None, dry_run: bool = False) -> Dict[str, int]:
        """
        Send to a list of email addresses directly.
        """
        if not self.backend:
            print("[email_sender] No email backend configured.")
            return {'sent': 0, 'failed': 0, 'skipped': 0}
        
        # Check daily limit
        remaining, sent_today = self.email_manager.get_emails_to_send(limit=50)
        
        if remaining <= 0:
            print(f"[email_sender] Daily limit reached")
            return {'sent': 0, 'failed': 0, 'skipped': len(recipient_list)}
        
        # Limit recipients
        recipient_list = recipient_list[:remaining]
        
        stats = {'sent': 0, 'failed': 0, 'skipped': 0}
        
        for idx, recipient in enumerate(recipient_list, 1):
            if dry_run:
                print(f"[DRY RUN] Would send email to {recipient}")
                stats['sent'] += 1
                continue
            
            try:
                body = message_template or f"Job lead information for {recipient}"
                
                if self.backend == "sendgrid":
                    success = self._send_via_sendgrid(recipient, subject, body)
                elif self.backend == "smtp":
                    success = self._send_via_smtp(recipient, subject, body)
                else:
                    success = False
                
                if success:
                    self.email_manager.mark_email_sent("system", recipient, subject, "success")
                    stats['sent'] += 1
                else:
                    stats['failed'] += 1
                
                time.sleep(1)
            
            except Exception as e:
                stats['failed'] += 1
                if self.verbose:
                    print(f"Error sending to {recipient}: {e}")
        
        return stats
    
    def _format_message(self, email_data: Dict, template: str = None) -> str:
        """Format email message body"""
        if template:
            return template.format(**email_data)
        
        domains = email_data.get('domains', '')
        job_titles = email_data.get('job_titles', '')
        
        body = f"""Hello,

We found your email through recent job postings and wanted to reach out.

Company Domains: {domains}
Related Job Titles: {job_titles}

If you're interested in discussing opportunities, please let us know.

Best regards,
Lead Finder Team
"""
        return body
    
    def _send_via_sendgrid(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            return response.status_code in [200, 201, 202]
        
        except Exception as e:
            if self.verbose:
                print(f"[email_sender] SendGrid error: {e}")
            return False
    
    def _send_via_smtp(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via SMTP"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            config = self.smtp_config
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(config['host'], config['port']) as server:
                server.starttls()
                server.login(config['user'], config['password'])
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            if self.verbose:
                print(f"[email_sender] SMTP error: {e}")
            return False
    
    def get_daily_stats(self) -> Dict:
        """Get today's email statistics"""
        return self.email_manager.get_daily_stats()
