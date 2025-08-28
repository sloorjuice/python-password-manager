import json
import os

PWDB = 'passwords.json'

def load_data():
    if not os.path.exists(PWDB):
        return {}
    with open(PWDB, "r") as f:
        return json.load(f)

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
        # no master password yet -> set it up
        master = input("Set a master password: ")
        data["master"] = master
        data["accounts"] = {} # ensure accounts section exists
        save_data(data)
        print("Master password set!")
        return data["master"]

def main():
    data = load_data()
    get_master_password(data)
    login_user(data)

    while True:
        print("\nOptions: quit")
        choice = input("> ")

        if choice == "quit":
            break
        else:
            print("Not a valid command.")

if __name__ == "__main__":
    main()






















