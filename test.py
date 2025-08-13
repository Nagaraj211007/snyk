import os
import pickle
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# --- Vulnerability 1: Command Injection ---
@app.route('/ping', methods=['GET'])
def ping():
    ip = request.args.get('ip', '')
    result = os.popen(f'ping -c 1 {ip}').read()  # ⚠️ Unsanitized input
    return f"<pre>{result}</pre>"

# --- Vulnerability 2: Insecure Deserialization ---
@app.route('/load', methods=['POST'])
def load():
    data = request.data
    obj = pickle.loads(data)  # ⚠️ Arbitrary code execution possible
    return f"Loaded: {obj}"

# --- Vulnerability 3: SQL Injection ---
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)  # ⚠️ Vulnerable to SQL injection
    user = c.fetchone()
    conn.close()
    
    if user:
        return f"Welcome, {user[0]}!"
    else:
        return "Login failed"

if __name__ == '__main__':
    app.run(debug=True)
