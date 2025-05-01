
import mysql.connector
from decimal import Decimal  
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jul040607!",  
    database="onlinebanking"          
)
cursor = db.cursor()  


def login():
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    
    query = "SELECT * FROM Accounts WHERE account_number = %s AND pin = %s"
    cursor.execute(query, (account_number, pin))
    user = cursor.fetchone()  

    if user: 
        print(f"\nLogin successful. Welcome back, {user[2]}!")
        return user
    else:
        print("\nIncorrect account number or PIN. Please try again.")
        return None

def create_account():
    account_number = input("Choose a new account number: ")
    pin = input("Set a PIN: ")
    full_name = input("Enter your full name: ")

   
    cursor.execute("SELECT * FROM Accounts WHERE account_number = %s", (account_number,))
    if cursor.fetchone():  
        print("Account number already exists. Try again.")
    else:
        
        cursor.execute("INSERT INTO Accounts (account_number, pin, full_name, balance) VALUES (%s, %s, %s, %s)",
                       (account_number, pin, full_name, 0.00)) 
        db.commit() 
        print("Account created successfully!")


def check_balance(account_number):
    cursor.execute("SELECT balance FROM Accounts WHERE account_number = %s", (account_number,))
    balance = cursor.fetchone()
    if balance:
        print(f"\nYour current balance is: ${balance[0]:.2f}")
    else:
        print("\nAccount not found.")


def deposit(account_number):
    try:
        amount = float(input("Enter the amount to deposit: "))  
        if amount <= 0:  
            print("\nDeposit amount must be greater than 0.")
            return

        
        amount = Decimal(str(amount))
        
        cursor.execute("SELECT balance FROM Accounts WHERE account_number = %s", (account_number,))
        balance = cursor.fetchone()
        if balance:
            new_balance = Decimal(balance[0]) + amount  
            cursor.execute("UPDATE Accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            db.commit()
            print(f"Deposit successful! Your new balance is: ${new_balance:.2f}")
        else:
            print("\nAccount not found.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def withdraw(account_number):
    try:
        amount = float(input("Enter the amount to withdraw: "))  
        if amount <= 0:  
            print("\nWithdrawal amount must be greater than 0.")
            return

    
        amount = Decimal(str(amount))
        
        cursor.execute("SELECT balance FROM Accounts WHERE account_number = %s", (account_number,))
        balance = cursor.fetchone()
        if balance:
            current_balance = Decimal(balance[0])
            if amount > current_balance:  
                print("\nInsufficient funds. Withdrawal canceled.")
            else:
                new_balance = current_balance - amount  
                cursor.execute("UPDATE Accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
                db.commit()
                print(f"Withdrawal successful! Your new balance is: ${new_balance:.2f}")
        else:
            print("\nAccount not found.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def edit_account(account_number):
    print("\n1. Change Name")
    print("2. Change PIN")
    choice = input("Choose an option (1-2): ")

    if choice == "1":
        new_name = input("Enter your new name: ")
        cursor.execute("UPDATE Accounts SET full_name = %s WHERE account_number = %s", (new_name, account_number))
        db.commit()
        print("\nName updated successfully!")
    elif choice == "2":
        new_pin = input("Enter your new PIN: ")
        cursor.execute("UPDATE Accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
        db.commit()
        print("\nPIN updated successfully!")
    else:
        print("\nInvalid choice.")


def close_account(account_number):
    confirmation = input("Are you sure you want to close your account? (yes/no): ")
    if confirmation.lower() == "yes":
        cursor.execute("DELETE FROM Accounts WHERE account_number = %s", (account_number,))
        db.commit()
        print("\nYour account has been closed.")
    else:
        print("\nAccount closure canceled.")


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
                print("\nWhat would you like to do?")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Edit Account Information")
                print("5. Close Account")
                print("6. Logout")
                
                option = input("Enter your choice (1-6): ")

                if option == "1":
                    check_balance(account_number)
                elif option == "2":
                    deposit(account_number)
                elif option == "3":
                    withdraw(account_number)
                elif option == "4":
                    edit_account(account_number)
                elif option == "5":
                    close_account(account_number)
                    break
                elif option == "6":
                    print("\nThank you for using SmartBank. Goodbye!")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
    elif choice == "2": 
        create_account()
    elif choice == "3":  
        print("Goodbye!")
    else:
        print("\nInvalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
