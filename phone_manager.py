"""
Phone number management and export
"""
import csv
import json
from datetime import datetime
from typing import Dict, List, Set


class PhoneManager:
    """Manage and export extracted phone numbers"""
    
    def __init__(self, output_dir: str = "output", verbose: bool = False):
        self.output_dir = output_dir
        self.verbose = verbose
    
    def export_phones_to_csv(self, phones: Dict[str, Dict], filepath: str) -> int:
        """Export phone numbers to CSV file"""
        if not phones:
            if self.verbose:
                print("[phone_manager] No phones to export")
            return 0
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Phone Number', 'Sources', 'Job Titles'])
                
                for phone, info in phones.items():
                    sources = len(info.get('sources', []))
                    titles = ', '.join(list(info.get('job_titles', set()))[:3])
                    writer.writerow([phone, sources, titles])
            
            if self.verbose:
                print(f"[phone_manager] Exported {len(phones)} phones to {filepath}")
            
            return len(phones)
        
        except Exception as e:
            if self.verbose:
                print(f"[phone_manager] Error exporting phones: {e}")
            return 0
    
    def export_phones_to_json(self, phones: Dict[str, Dict], filepath: str) -> int:
        """Export phone numbers to JSON file"""
        if not phones:
            if self.verbose:
                print("[phone_manager] No phones to export")
            return 0
        
        try:
            # Convert sets to lists for JSON serialization
            json_data = {}
            for phone, info in phones.items():
                json_data[phone] = {
                    'phone': phone,
                    'sources': list(info.get('sources', [])),
                    'job_titles': list(info.get('job_titles', set()))
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            if self.verbose:
                print(f"[phone_manager] Exported {len(phones)} phones to {filepath}")
            
            return len(phones)
        
        except Exception as e:
            if self.verbose:
                print(f"[phone_manager] Error exporting phones: {e}")
            return 0


def filter_and_dedupe_phones(job_phones: Dict) -> Dict[str, Dict]:
    """
    Filter duplicates and organize phone numbers.
    Returns dict with unique phones mapped to job sources.
    """
    all_phones = {}
    
    for domain, info in job_phones.items():
        for phone in info.get('phones', set()):
            if phone not in all_phones:
                all_phones[phone] = {
                    'phone': phone,
                    'domains': set(),
                    'sources': [],
                    'job_titles': set()
                }
            
            all_phones[phone]['domains'].add(domain)
            if info.get('job_url'):
                all_phones[phone]['sources'].append(info['job_url'])
            if info.get('title'):
                all_phones[phone]['job_titles'].add(info['title'])
    
    return all_phones
