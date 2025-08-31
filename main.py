import json, os, getpass, secrets, string, re, base64, hashlib
from cryptography.fernet import Fernet

DATABASE_FILE = 'configs/passwords.json'
SALT_FILE = 'configs/salt.bin'

# -----------------------------ENCRYPTION-----------------------------

def generate_salt():
    return secrets.token_bytes(16)

def save_salt(salt):
    ensure_configs_dir()
    with open(SALT_FILE, 'wb') as f:
        f.write(salt)
        
def load_salt():
    if not os.path.exists(SALT_FILE):
        return None
    with open(SALT_FILE, 'rb') as f:
        return f.read()

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    # PBKDF2 with SHA256, 100,000 iterations
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100_000,
        dklen=32
    )
    return base64.urlsafe_b64encode(key)

def encrypt_password(pw: str, key: bytes) -> bytes:
    """Encrypt the password using the provided key."""
    f = Fernet(key)
    return f.encrypt(pw.encode()).decode()

def decrypt_password(encrypted_pw: str, key: bytes) -> str:
    """Decrypt the password using the provided key."""
    try:
        f = Fernet(key)
        return f.decrypt(encrypted_pw.encode()).decode()
    except Exception as e:
        print(f"Error: Unable to decrypt password. Wrong key or corrupted data: {e}")
        return ""

# -----------------------------CONFIGURATION-----------------------------

def load_data() -> dict:
    """Load data from a JSON file and return it."""
    try:
        if not os.path.exists(DATABASE_FILE):
            return {}
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: Password database is corrupted.")
        return {}
    except Exception as e:
        print(f"Error trying to load data: {e}")
        return {}

def ensure_configs_dir():
    """Ensure the configs directory exists."""
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)

def save_data(data: dict):
    """Save data to a JSON file."""
    try:
        ensure_configs_dir()
        with open(DATABASE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error trying to save data: {e}")

def check_master_password(data: dict):
    """
    Get the master password from the user.
    If no master password set one up.
    """
    if "master" not in data:
        master = getpass.getpass("Set a master password: ")
        
        salt = generate_salt()
        save_salt(salt)
        key = derive_key_from_password(master, salt)
        e_master = encrypt_password(master, key)
  
        # # Generate and save the encryption key      
        # ensure_configs_dir()
        # key = Fernet.generate_key()
        # with open(KEY_FILE, "wb") as key_file:
        #     key_file.write(key)
    
        # e_master = encrypt_password(master, key)
        data["master"] = e_master
        data["accounts"] = [] # ensure accounts section exists
        save_data(data)
        print("Master password set!")

# -----------------------------ACCOUNT MANAGEMENT-----------------------------

def login_user(data: dict) -> str:
    """Log in the user by verifying the master password."""
    attempt = getpass.getpass("Enter master password: ")

    salt = load_salt()
    if not salt:
        print("No salt found! Exiting.")
        exit()
    key = derive_key_from_password(attempt, salt)
    master = decrypt_password(data.get("master"), key)

    # ensure_configs_dir()
    # key = load_key()
    # master = decrypt_password(data.get("master"), key)

    if attempt != master:
        print("Incorrect master password! Exiting.")
        exit()

    print("Access Granted.")
    return attempt

def validate_email(email: str) -> bool:
    """Email validation using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

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
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    pw_length = 16
    pw = ''.join(secrets.choice(characters) for i in range(pw_length))
    return pw

def save_account(title: str, identifier: str, pw: str, account_type: str, mpw: str, data: dict):
    """Save a new account."""
    salt = load_salt()
    key = derive_key_from_password(mpw, salt)
    encrypted_pw = encrypt_password(pw, key)
    new_account = {
        "title": title,
        account_type: identifier,
        "password": encrypted_pw
    }

    data["accounts"].append(new_account)
    save_data(data)
    print("Saved Account.")

def remove_account(data: dict):
    """Remove an existing account."""
    title = input("Enter the title of the account to remove: ")
    found = False
    for account in data.get("accounts", []):
        if account["title"] == title:
            data["accounts"].remove(account)
            save_data(data)
            print("Account removed.")
            found = True
            break
    if not found:
        print("Account not found.")

def list_accounts(master_pw: str, data: dict):
    """List all saved accounts."""
    salt = load_salt()
    key = derive_key_from_password(master_pw, salt)
    for account in data["accounts"]:
        decrypted_pw = decrypt_password(account["password"], key)
        if account.get("email"):
            print(f"{account['title']}: Email: {account['email']}, Password: {decrypted_pw}")
        else:
            print(f"{account['title']}: Username: {account['username']}, Password: {decrypted_pw}")

def setup_account(master_pw: str, data: dict):
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
        save_account(title, identifier, pw, account_type, master_pw, data)

    elif choice.lower() == 'y':
        pw = generate_pw()
        print(f"Generated password for {title}: {pw}")
        save_account(title, identifier, pw, account_type, master_pw, data)
    else:
        print("Invalid choice.")

def main():
    try:
        data = load_data()
        check_master_password(data)
        master_pw = login_user(data)

        while True:
            print("\nOptions: quit, save, remove, list")
            choice = input("> ")

            if choice == "quit":
                break
            elif choice == "save":
                setup_account(master_pw, data)
            elif choice == "list":
                list_accounts(master_pw, data)
            elif choice == "remove":
                remove_account(data)
            else:
                print("Not a valid command.")
    except KeyboardInterrupt:
        print("\n^C detected. Exiting program.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()






















