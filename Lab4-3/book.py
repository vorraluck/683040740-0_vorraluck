from library_item import LibraryItem

class Book(LibraryItem):
    def __init__(self, title, item_id, author): #ทำงานทันทีเมื่อสร้างออบเจ้กของคลาส
        super().__init__(title, item_id) 
        self.author = author #สร้างตัวแปรผู้แต่ง
        self.pages_count = 0 


    def set_pages_count(self, pages): 
        self.pages_count = pages 

    def display_info(self): 
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Status: {self.get_status()}")  
