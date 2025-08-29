import json
import os

PWDB = 'passwords.json'

def load_data():
    try:
        if not os.path.exists(PWDB):
            return {}
        with open(PWDB, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error trying to load data: {e}")

def save_data(data):
    try:
        with open(PWDB, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error trying to get data {e}")

def login_user(data):
    attempt = input("Enter master password: ")

    master = data.get("master")

    if attempt != master:
        print("Incorrect master password! Exiting.")
        exit()

    print("Access Granted.")


def get_master_password(data):
    if "master" not in data:
        master = input("Set a master password: ")
        data["master"] = master
        data["accounts"] = [] # ensure accounts section exists
        save_data(data)
        print("Master password set!")
        return

def list_accounts(data):
    for account in data["accounts"]:
        print(f"{account['title']}: Email: {account['email']}, Password: {account['password']}")

def validate_email(email):
    return True

def validate_pw(pw):
    return True

def save_account(title, email, pw, data):
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
            title = input("Whats a title for your account? (e.g. Website, App, etc)")
            email = input(f"Whats your email for {title}? ")
            pw = input(f"Whats your password for {title}? ")
            save_account(title, email, pw, data)
        elif choice == "list":
            list_accounts(data)
        else:
            print("Not a valid command.")

if __name__ == "__main__":
    main()






















