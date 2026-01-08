from book import Book
from textbook import TextBook
from magazine import Magazine

print("---- Book Test ----")
book = Book("Harry Potter", "B001", "J.K. Rowling")
book.set_pages_count(350)
book.display_info()
book.check_out()
book.display_info()

print("\n---- TextBook Test ----")
textbook = TextBook("Physics", "T001", "Serway", "Science", 12)
textbook.set_pages_count(500)
textbook.display_info()
textbook.check_out()
textbook.display_info()
textbook.return_item()
textbook.display_info()

print("\n---- Magazine Test ----")
magazine = Magazine("National Geographic", "M001", 202)
magazine.display_info()
magazine.check_out()
magazine.display_issue()
