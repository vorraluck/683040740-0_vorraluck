from cat import Cat
from datetime import datetime, timedelta

c1 = Cat("Mochi", 2, "Alice")
c2 = Cat("Sushi", 4, "Bob")
c3 = Cat("Tofu", 1, "Charlie")


print(f"Cat 1 Date In: {c1.date_in}")
c1.greet()


print(f"Cat 2 Date Out (Original): {c2.date_out}")
# บวกเวลาเพิ่มไปอีก 2 วัน
c2.date_out = c2.date_out + timedelta(days=2)
print(f"Cat 2 Date Out (Updated): {c2.date_out}")


c3.owner = "David"
c3.age = 3

print("\n--- All Cats Details ---")
c1.show_info()
c2.show_info()
c3.show_info()

print(f"Total number of cats: {Cat.count}")

Cat.count = 0
print("Resetting cat count...")


print(f"Total number of cats after reset: {Cat.count}")