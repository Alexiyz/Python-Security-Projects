import hashlib
import getpass

password_manager = {}

def create_account():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    password_manager[username] = hashed_password
    print("Account created")

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in password_manager.keys() and password_manager[username] == hashed_password:
        print("Welcome " + username)
    else:
        print("Invalid username or password")

def main():
    while True:
        user_choice = input("Enter 1 to create an account, 2 to login, 3 to exit: ")
        if user_choice == "1":
            create_account()
        elif user_choice == "2":
            login()
        elif user_choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
