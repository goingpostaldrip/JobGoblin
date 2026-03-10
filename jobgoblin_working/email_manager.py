# JobGoblin Working - Email Manager
# Add email management logic here if needed for future enhancements.

class EmailManager:
    def __init__(self):
        self.emails = []

    def add_email(self, email):
        self.emails.append(email)

    def get_emails(self):
        return self.emails
