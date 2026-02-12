from datetime import datetime
class Cat:
    total_cats = 0   # class variable

    def __init__(self, name, owner, age):
        self.name = name
        self.owner = owner
        self.age = age
        self.date_in = datetime.now()
        self.date_out = None
        Cat.total_cats += 1

    def greet(self):
        print(f"Meow! I'm {self.name} 🐱")

    def show_details(self):
        print("----- Cat Details -----")
        print(f"Name     : {self.name}")
        print(f"Owner    : {self.owner}")
        print(f"Age      : {self.age}")
        print(f"Date in  : {self.date_in}")
        print(f"Date out : {self.date_out}")
        print("-----------------------")

    @classmethod
    def get_total_cats(cls):
        return cls.total_cats

    @classmethod
    def reset_total_cats(cls):
        cls.total_cats = 0
