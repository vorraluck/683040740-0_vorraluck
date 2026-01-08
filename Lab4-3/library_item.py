class LibraryItem:
    def __init__(self, title, item_id): 
        self.title = title
        self.id = item_id
        self.checked_out = False 

    def get_status(self): 
        return "Checked out" if self.checked_out else "Available"

    def check_out(self):
        if not self.checked_out:
            self.checked_out = True
            return True
        return False

    def return_item(self):
        if self.checked_out:
            self.checked_out = False
            return True
        return False

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"ID: {self.id}")
        print(f"Status: {self.get_status()}")