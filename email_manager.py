"""
Email manager - handles CSV export, tracking, and 50-per-day limit
"""
import csv
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set
from pathlib import Path

class EmailManager:
    """Manages email collection, CSV export, and daily sending limits"""
    
    def __init__(self, output_dir: str = "output", verbose: bool = False):
        self.output_dir = output_dir
        self.verbose = verbose
        self.emails_sent_today_file = os.path.join(output_dir, ".emails_sent_today.json")
        self.email_history_file = os.path.join(output_dir, "email_send_history.json")
        self.emails_csv_file = os.path.join(output_dir, "found_emails.csv")
        
        os.makedirs(output_dir, exist_ok=True)
    
    def export_emails_to_csv(self, emails_data: Dict, filename: str = None) -> str:
        """
        Export extracted emails to CSV file.
        emails_data: dict mapping email -> {'email': str, 'domains': set, 'sources': list, 'job_titles': set}
        """
        if not filename:
            filename = self.emails_csv_file
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'email', 'domains', 'sources_count', 'job_titles', 'first_seen', 'last_updated'
                ])
                writer.writeheader()
                
                for email, info in emails_data.items():
                    domains = ', '.join(sorted(info.get('domains', set())))
                    job_titles = ', '.join(sorted(list(info.get('job_titles', set()))[:3]))  # First 3 titles
                    sources = info.get('sources', [])
                    
                    writer.writerow({
                        'email': email,
                        'domains': domains,
                        'sources_count': len(sources),
                        'job_titles': job_titles,
                        'first_seen': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat()
                    })
            
            if self.verbose:
                print(f"[email_manager] Exported {len(emails_data)} emails to {filename}")
            
            return filename
        
        except Exception as e:
            print(f"[email_manager] Error exporting to CSV: {e}")
            return ""
    
    def load_emails_from_csv(self, filename: str = None) -> Dict[str, Dict]:
        """Load previously exported emails from CSV"""
        if not filename:
            filename = self.emails_csv_file
        
        if not os.path.exists(filename):
            return {}
        
        emails = {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('email', '').strip()
                    if email:
                        emails[email] = {
                            'email': email,
                            'domains': set(d.strip() for d in row.get('domains', '').split(',') if d.strip()),
                            'sources_count': int(row.get('sources_count', 0)),
                            'job_titles': row.get('job_titles', ''),
                            'first_seen': row.get('first_seen', ''),
                            'last_updated': row.get('last_updated', '')
                        }
            
            if self.verbose:
                print(f"[email_manager] Loaded {len(emails)} emails from {filename}")
            
            return emails
        
        except Exception as e:
            print(f"[email_manager] Error loading from CSV: {e}")
            return {}
    
    def get_emails_to_send(self, limit: int = 50) -> List[str]:
        """
        Get list of emails to send today (up to limit).
        Respects daily sending limit.
        """
        sent_today = self._get_emails_sent_today()
        
        if len(sent_today) >= limit:
            print(f"[email_manager] Daily limit ({limit}) reached. Already sent {len(sent_today)} emails today.")
            return []
        
        remaining = limit - len(sent_today)
        return remaining, sent_today
    
    def mark_email_sent(self, email: str, recipient_email: str = "", subject: str = "", status: str = "success"):
        """Mark an email as sent for today's limit"""
        sent_today = self._get_emails_sent_today()
        
        sent_today.append({
            'email': email,
            'recipient_email': recipient_email,
            'subject': subject,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_emails_sent_today(sent_today)
        
        # Also log to history file
        self._log_email_send(email, recipient_email, subject, status)
    
    def _get_emails_sent_today(self) -> List[Dict]:
        """Get list of emails sent today"""
        if not os.path.exists(self.emails_sent_today_file):
            return []
        
        try:
            with open(self.emails_sent_today_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check if data is from today
                if data and 'date' in data:
                    saved_date = datetime.fromisoformat(data['date']).date()
                    today = datetime.now().date()
                    
                    if saved_date == today:
                        return data.get('emails_sent', [])
                    else:
                        # Reset if date has changed
                        return []
            
            return []
        
        except Exception as e:
            if self.verbose:
                print(f"[email_manager] Error loading sent emails: {e}")
            return []
    
    def _save_emails_sent_today(self, sent_list: List[Dict]):
        """Save today's sent emails"""
        try:
            data = {
                'date': datetime.now().isoformat(),
                'emails_sent': sent_list
            }
            with open(self.emails_sent_today_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[email_manager] Error saving sent emails: {e}")
    
    def _log_email_send(self, email: str, recipient_email: str, subject: str, status: str):
        """Log email send to history file"""
        try:
            history = []
            if os.path.exists(self.email_history_file):
                with open(self.email_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            history.append({
                'email': email,
                'recipient_email': recipient_email,
                'subject': subject,
                'status': status,
                'timestamp': datetime.now().isoformat()
            })
            
            with open(self.email_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
        
        except Exception as e:
            if self.verbose:
                print(f"[email_manager] Error logging send: {e}")
    
    def reset_daily_limit(self):
        """Reset daily sending limit (call at midnight or manually)"""
        if os.path.exists(self.emails_sent_today_file):
            try:
                os.remove(self.emails_sent_today_file)
                if self.verbose:
                    print("[email_manager] Daily limit reset")
            except:
                pass
    
    def get_daily_stats(self) -> Dict:
        """Get today's email sending statistics"""
        sent_today = self._get_emails_sent_today()
        
        return {
            'emails_sent_today': len(sent_today),
            'daily_limit': 50,
            'remaining': max(0, 50 - len(sent_today)),
            'success_count': len([e for e in sent_today if e.get('status') == 'success']),
            'failed_count': len([e for e in sent_today if e.get('status') != 'success'])
        }
