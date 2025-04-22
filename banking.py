import mysql.connector
import bcrypt  
from decimal import Decimal  


db = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="Jul040607!",  
    database="smartbank"  
)
cursor = db.cursor()

def login():
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")


    query = "SELECT * FROM Accounts WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(pin.encode('utf-8'), user[1].encode('utf-8')):  # Verify PIN
        print(f"\nLogin successful. Welcome back, {user[2]}!")
        return user
    else:
        print("\nIncorrect account number or PIN.")
        return None

def create_account():
    new_account_number = input("Enter a new account number: ")
    new_pin = input("Set a PIN: ")
    full_name = input("Enter your full name: ")


    hashed_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("SELECT * FROM Accounts WHERE account_number = %s", (new_account_number,))
    if cursor.fetchone():
        print("Account number already exists. Try again.")
    else:
        cursor.execute("INSERT INTO Accounts (account_number, pin, full_name, balance) VALUES (%s, %s, %s, %s)",
                       (new_account_number, hashed_pin, full_name, 0.00))
        db.commit()
        print("Account created successfully! You can now log in.")

def close_account(account_number):
    confirmation = input("Are you sure you want to close your account? (yes/no): ").lower()
    if confirmation == "yes":
        cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account_number,))
        db.commit()
        print("Your account has been closed.")
    else:
        print("Account closure canceled.")

def edit_account(account_number):
    print("1. Change Name")
    print("2. Change PIN")
    edit_choice = input("Choose an option to edit (1-2): ")

    if edit_choice == "1":
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE Accounts SET full_name = %s WHERE account_number = %s", (new_name, account_number))
        db.commit()
        print("Name updated successfully.")
    elif edit_choice == "2":
        new_pin = input("Enter new PIN: ")
        hashed_pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE Accounts SET pin = %s WHERE account_number = %s", (hashed_pin, account_number))
        db.commit()
        print("PIN updated successfully.")
    else:
        print("Invalid choice.")

def main():
    print("Welcome to SmartBank!")
    print("1. Log In")
    print("2. Create New Account")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        user = login()
        if user:
            account_number = user[0]
            while True:
                print("\nChoose an option:")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Edit Account Information")
                print("5. Close Account")
                print("6. Exit")

                option = input("Enter your choice (1-6): ")

                if option == "1":
                    print(f"\nYour balance is ${user[3]:.2f}")
                elif option == "2":  
                    amount = float(input("Enter deposit amount: "))
                    
                    
                    if amount <= 0:
                        print("Deposit amount must be positive.")
                    else:
                        
                        amount = Decimal(amount)

                        
                        new_balance = Decimal(user[3]) + amount
                        
                        
                        cursor.execute("UPDATE Accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
                        db.commit()

                        
                        cursor.execute("SELECT * FROM Accounts WHERE account_number = %s", (account_number,))
                        user = cursor.fetchone()

                        print(f"Deposit successful. New balance: ${user[3]:.2f}")
                elif option == "3":  
                    amount = float(input("Enter withdrawal amount: "))
                    amount = Decimal(amount)  

                    if amount > user[3]:
                        print("Not enough funds.")
                    else:
                        new_balance = user[3] - amount  
                        cursor.execute("UPDATE Accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
                        db.commit()

                        cursor.execute("SELECT * FROM Accounts WHERE account_number = %s", (account_number,))
                        user = cursor.fetchone()

                        print(f"Withdrawal successful. New balance: ${user[3]:.2f}")
                elif option == "4":
                    edit_account(account_number)
                elif option == "5":
                    close_account(account_number)
                    break
                elif option == "6":
                    print("Thank you for using SmartBank. Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.")
        else:
            print("Login failed. Returning to main menu.")
    
    elif choice == "2":
        create_account()

    elif choice == "3":
        print("Goodbye!")

    else:
        print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
