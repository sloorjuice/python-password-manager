import json
import os
import getpass

PWDB = 'passwords.json'

def load_data() -> dict:
    """Load data from a JSON file and return it."""
    try:
        if not os.path.exists(PWDB):
            return {}
        with open(PWDB, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error trying to load data: {e}")

def save_data(data: dict):
    """Save data to a JSON file."""
    try:
        with open(PWDB, "w") as f:
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
        print(f"{account['title']}: Email: {account['email']}, Password: {account['password']}")

def validate_email(email: str) -> bool:
    # Basic email validation
    return "@" in email and "." in email

def validate_pw(pw: str) -> bool:
    """Check the password strength."""
    return True

def save_account(title: str, email: str, pw: str, data: dict):
    """Save a new account."""
    if validate_email(email) and validate_pw(pw):
        new_account = {
            "title": title,
            "email": email,
            "password": pw
        }

        data["accounts"].append(new_account)
        save_data(data)
        print("Saved Account.")

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
            title = input("Whats a title for your account? (e.g. Website, App, etc) ")
            email = input(f"Whats your email (or username) for {title}? ")
            pw = getpass.getpass(f"Whats your password for {title}? ")
            save_account(title, email, pw, data)
        elif choice == "list":
            list_accounts(data)
        else:
            print("Not a valid command.")

if __name__ == "__main__":
    main()






















