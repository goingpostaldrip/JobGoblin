# JobGoblin Working - Phone Manager
# Add phone management logic here if needed for future enhancements.

class PhoneManager:
    def __init__(self):
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def get_phones(self):
        return self.phones
