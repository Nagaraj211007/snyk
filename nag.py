import os
import sqlite3

# --- Hardcoded Credentials ---
USERNAME = "admin"
PASSWORD = "password123"

# --- Insecure Login ---
def login():
    user = input("Username: ")
    pwd = input("Password: ")

    if user == USERNAME and pwd == PASSWORD:
        print("Login successful!")
    else:
        print("Access denied.")

# --- SQL Injection Vulnerability ---
def search_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    name = input("Enter name to search: ")
    query = f"SELECT * FROM users WHERE name = '{name}'"
    print(f"Running query: {query}")
    try:
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
    except sqlite3.Error as e:
        print("Database error:", e)
    conn.close()

# --- Command Injection ---
def run_command():
    cmd = input("Enter a shell command to run: ")
    os.system(cmd)

# --- Insecure File Handling ---
def read_file():
    filename = input("Enter filename to read: ")
    with open(filename, 'r') as f:
        print(f.read())

# --- Main Menu ---
def main():
    while True:
        print("\n1. Login\n2. Search Users\n3. Run Command\n4. Read File\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            search_users()
        elif choice == "3":
            run_command()
        elif choice == "4":
            read_file()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
