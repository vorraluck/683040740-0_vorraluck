from datetime import datetime
from library_item import LibraryItem

class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number

        now = datetime.now()
        self.month = now.month
        self.year = now.year

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"ID: {self.id}")
        print(f"Issue Number: {self.issue_number}")
        print(f"Month: {self.month}")
        print(f"Year: {self.year}")
        print(f"Status: {self.get_status()}")

    def display_issue(self):
        self.display_info()
