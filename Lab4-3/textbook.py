from book import Book

class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level

    def display_course_info(self): 
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print(f"Status: {self.get_status()}")

    
    def display_info(self): 
        self.display_course_info()
