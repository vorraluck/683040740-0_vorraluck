from bank_template import BankAccount

john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)
sarah = BankAccount("Sarah", "saving", 0)

accounts = [john, tim, sarah]

john.deposit(3000)
print("John current balance:", john.balance)

tim.deposit(500_000)
print("Tim current balance:", tim.balance)

sarah.deposit(50_000_000)

sarah_loan = BankAccount("Sarah", "loan", -100_000_000)
accounts.append(sarah_loan)

# Show all account information 
print("\n--- All Accounts ---")
for acc in accounts:
    acc.print_customer()