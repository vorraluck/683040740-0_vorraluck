from cat import Cat
from datetime import datetime, timedelta

# Add 3 cats
cat1 = Cat("Milo", "Alice", 2)
cat2 = Cat("Luna", "Bob", 4)
cat3 = Cat("Oliver", "Charlie", 1)

# -------- First cat --------
print("First cat date_in:")
print(cat1.date_in)

cat1.greet()

# -------- Second cat --------
print("\nSecond cat date_out (before):")
print(cat2.date_out)

cat2.date_out = datetime.now() + timedelta(days=2)

print("Second cat date_out (after +2 days):")
print(cat2.date_out)

# -------- Third cat --------
cat3.owner = "Diana"
cat3.age = 3

# -------- Show all cats --------
print("\nAll cats details:")
cat1.show_details()
cat2.show_details()
cat3.show_details()

# -------- Total cats --------
print("Total number of cats:")
print(Cat.get_total_cats())

# -------- Reset total cats --------
Cat.reset_total_cats()

print("Total number of cats after reset:")
print(Cat.get_total_cats())
