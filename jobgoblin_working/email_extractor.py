# JobGoblin Working - Email Extractor
# Add email extraction logic here if needed for future enhancements.

import re

def extract_emails(text):
    return re.findall(r"[\w\.-]+@[\w\.-]+", text)
