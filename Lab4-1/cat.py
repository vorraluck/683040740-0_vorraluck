from datetime import datetime

class Cat:
    
    count = 0

    def __init__(self, name, age, owner):
        self.name = name
        self.age = age
        self.owner = owner
        self.date_in = datetime.now()  
        self.date_out = datetime.now() 
        Cat.count += 1

    def greet(self):
        print(f"Meow! My name is {self.name}. Nice to meet you!")

    def show_info(self):
        print(f"Cat: {self.name} | Age: {self.age} | Owner: {self.owner}")
        print(f"Check-in: {self.date_in.strftime('%Y-%m-%d %H:%M')}")
        print(f"Check-out: {self.date_out.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 30)