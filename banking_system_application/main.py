from decimal import Decimal, getcontext
from database.connection import DatabaseConnection
from models.user import User
from models.account import Account
from utils.validators import validate_password

# Set Decimal precision
getcontext().prec = 28


def display_menu():
    print("\n=== BANKING SYSTEM ===")
    print("1. Add User")
    print("2. Show Users")
    print("3. Login")
    print("4. Exit")


def display_login_menu():
    print("\n=== USER MENU ===")
    print("1. Show Balance")
    print("2. Show Transactions")
    print("3. Credit Amount")
    print("4. Debit Amount")
    print("5. Transfer Amount")
    print("6. Active/Deactivate Account")
    print("7. Change Password")
    print("8. Update Profile")
    print("9. Logout")


def get_valid_password():
    while True:
        password = input("Enter password: ")
        is_valid, message = validate_password(password)
        if is_valid:
            return password
        print(f"Invalid password: {message}")


def main():
    db = DatabaseConnection()
    user_manager = User(db)
    account_manager = Account(db)
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("\n=== ADD USER ===")
            name = input("Enter name: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            city = input("Enter city: ")
            password = get_valid_password()
            initial_balance = Decimal(input("Enter initial balance (min 2000): "))
            if initial_balance < 2000:
                print("Initial balance must be at least 2000.")
                continue
            contact = input("Enter contact number: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            
            result = user_manager.create_user(
                name, dob, city, password, initial_balance,
                contact, email, address
            )
            print(result)
            
        elif choice == '2':
            print("\n=== USER LIST ===")
            db.cursor.execute(
                'SELECT account_number, name, city, balance FROM users'
            )
            users = db.cursor.fetchall()
            for user in users:
                print(f"Account: {user[0]}, Name: {user[1]}, "
                      f"City: {user[2]}, Balance: {user[3]}")
                
        elif choice == '3':
            print("\n=== LOGIN ===")
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            user = account_manager.login(account_number, password)
            
            if user:
                print(f"\nWelcome {user[1]}!")
                while True:
                    display_login_menu()
                    login_choice = input("Enter your choice: ")
                    
                    if login_choice == '1':
                        balance = account_manager.get_balance(account_number)
                        print(f"Current balance: {balance}")
                        
                    elif login_choice == '2':
                        print("\n=== TRANSACTION HISTORY ===")
                        transactions = account_manager.get_transactions(account_number)
                        for trans in transactions:
                            print(f"Type: {trans[0]}, Amount: {trans[1]}, "
                                  f"Time: {trans[2]}")
                            
                    elif login_choice == '3':
                        amount = Decimal(input("Enter amount to credit: "))
                        if amount <= 0:
                            print("Amount must be greater than zero.")
                            continue
                        result = account_manager.update_balance(
                            account_number, amount, 'credit'
                        )
                        print(result[1])
                        
                    elif login_choice == '4':
                        amount = Decimal(input("Enter amount to debit: "))
                        if amount <= 0:
                            print("Amount must be greater than zero.")
                            continue
                        result = account_manager.update_balance(
                            account_number, amount, 'debit'
                        )
                        print(result[1])
                        
                    elif login_choice == '5':
                        to_account = input("Enter recipient account number: ")
                        amount = Decimal(input("Enter amount to transfer: "))
                        if amount <= 0:
                            print("Amount must be greater than zero.")
                            continue
                        result = account_manager.transfer_amount(
                            account_number, to_account, amount
                        )
                        print(result)
                        
                    elif login_choice == '6':
                        result = account_manager.toggle_account_status(account_number)
                        print(result)
                        
                    elif login_choice == '7':
                        old_password = input("Enter old password: ")
                        new_password = input("Enter new password: ")
                        result = account_manager.change_password(
                            account_number, old_password, new_password
                        )
                        print(result)
                        
                    elif login_choice == '8':
                        print("Enter new details (press enter to skip):")
                        city = input("City: ")
                        contact = input("Contact: ")
                        email = input("Email: ")
                        address = input("Address: ")
                        result = account_manager.update_profile(
                            account_number, city, contact, email, address
                        )
                        print(result)
                        
                    elif login_choice == '9':
                        print("Logged out successfully")
                        break
            else:
                print("Invalid credentials or account is deactivated")
                
        elif choice == '4':
            print("Thank you for using our banking system!")
            break
            
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
