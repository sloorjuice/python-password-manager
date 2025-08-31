import json
import os
import getpass
import secrets
import string
import re

DATABASE_FILE = 'passwords.json'

def load_data() -> dict:
    """Load data from a JSON file and return it."""
    try:
        if not os.path.exists(DATABASE_FILE):
            return {}
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error trying to load data: {e}")

def save_data(data: dict):
    """Save data to a JSON file."""
    try:
        with open(DATABASE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error trying to save data: {e}")

def login_user(data: dict):
    """Log in the user by verifying the master password."""
    attempt = getpass.getpass("Enter master password: ")

    master = data.get("master")

    if attempt != master:
        print("Incorrect master password! Exiting.")
        exit()

    print("Access Granted.")


def get_master_password(data: dict):
    """
    Get the master password from the user.
    If no master password set one up.
    """
    if "master" not in data:
        master = getpass.getpass("Set a master password: ")
        data["master"] = master
        data["accounts"] = [] # ensure accounts section exists
        save_data(data)
        print("Master password set!")
        return

def list_accounts(data: dict):
    """List all saved accounts."""
    for account in data["accounts"]:
        if account.get("email"):
            print(f"{account['title']}: Email: {account['email']}, Password: {account['password']}")
        else:
            print(f"{account['title']}: Username: {account['username']}, Password: {account['password']}")

def validate_email(email: str) -> bool:
    # Basic email validation
    return "@" in email and "." in email

def validate_pw(pw: str, min_length: int = 8) -> bool:
    """Check the password strength and length."""
    bad = False  # Initialize bad to False
    if len(pw) < min_length:
        print(f"Password should be at least {min_length} characters long.")
        bad = True
    if not re.search(r"[A-Z]", pw):
        print("Password doesn't contain at least one uppercase letter.")
        bad = True
    if not re.search(r"[a-z]", pw):
        print("Password doesn't contain at least one lowercase letter.")
        bad = True
    if not re.search(r"\d", pw):
        print("Password doesn't contain at least one digit.")
        bad = True
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        print("Password doesn't contain at least one special character.")
        bad = True
    if bad == True:
        return False
    return True

def generate_pw() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    pw_length = 16
    pw = ''.join(secrets.choice(characters) for i in range(pw_length))
    return pw

def save_account(title: str, identifier: str, pw: str, account_type: str, data: dict):
    """Save a new account."""
    new_account = {
        "title": title,
        account_type: identifier,
        "password": pw
    }

    data["accounts"].append(new_account)
    save_data(data)
    print("Saved Account.")

def setup_account(data: dict):
    """Set up a new account with a generated password."""
    title = input("Whats a title for your account? (e.g. Website, App, etc) ")
    
    identifier = input(f"Whats your email (or username) for {title}? ")
    if validate_email(identifier):
        account_type = "email"
    else:
        choice = input("This is not a valid email. Is this a username? (y/n) ")
        account_type = "username" if choice.lower() == "y" else "email"

    choice = input("Would you like to generate a password? (y/n) ")
    if choice.lower() == "n":
        while True:
            pw = getpass.getpass(f"Whats your password for {title}? ")
            if validate_pw(pw):
                break
            print("Password is not strong enough.")
            if input("Do you still want to use this password? (y/n) ").lower() == "y":
                break
            print("Please enter a new password.")
        save_account(title, identifier, pw, account_type, data)

    elif choice.lower() == 'y':
        pw = generate_pw()
        print(f"Generated password for {title}: {pw}")
        save_account(title, identifier, pw, account_type, data)
    else:
        print("Invalid choice.")

def main():
    data = load_data()
    get_master_password(data)
    login_user(data)

    while True:
        print("\nOptions: quit, save, list")
        choice = input("> ")

        if choice == "quit":
            break
        elif choice == "save":
            setup_account(data)
        elif choice == "list":
            list_accounts(data)
        else:
            print("Not a valid command.")

if __name__ == "__main__":
    main()






















