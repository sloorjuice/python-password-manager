# Python Password Manager CLI
This is a full Password Manager I created with Python.
Built with a quality CLI for easily saving, deleting, editing, viewing and exporting your account.
- Accounts can have emails and usernames, phone numbers coming soon.
- Passwords are stored in a Json with AES-128 encryption with fernett which also provides HMAC auth.
- The encryption key is derived from a Master Password using PBKDF2-HMAC-SHA256 with 100,000 iterations and a random salt.
- Easily export all your accounts into a CSV

## Setup Instructions

1. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**

   * On **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run your project**
   Replace this with your project’s run command, for example:

   ```bash
   python3 main.py
   ```
