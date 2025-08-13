import os
import sqlite3
import tempfile
import shlex
import subprocess
from pathlib import Path

# --- 1) Secrets & config ---
# Avoid hardcoding secrets; read from env or a secrets manager.
DB_PATH = os.environ.get("APP_DB_PATH", "app.db")

# --- 2) Safe database queries (prevents SQL injection) ---
def get_user_by_name(conn, name: str):
    # DO: use parameterized queries, never string concatenation.
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchone()

# --- 3) Safe file handling (prevents path traversal and race issues) ---
BASE_DIR = Path("uploads").resolve()  # fixed, known directory
BASE_DIR.mkdir(exist_ok=True)

def save_user_file(filename: str, content: bytes):
    # Allow only simple filenames; reject paths and weird segments.
    safe_name = Path(filename).name
    target = (BASE_DIR / safe_name).resolve()
    # Ensure final path stays inside BASE_DIR
    if not str(target).startswith(str(BASE_DIR)):
        raise ValueError("Invalid filename/path.")
    # Use atomic write via tempfile then replace
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    tmp_path.replace(target)
    return target

# --- 4) Safe subprocess usage (avoid command injection) ---
# Whitelist commands and arguments; use list form + no shell=True
ALLOWED_TOOLS = {"echo", "uptime"}

def run_tool(cmd: str, *args: str):
    if cmd not in ALLOWED_TOOLS:
        raise ValueError("Command not allowed.")
    # Validate args; here we only allow simple tokens
    clean_args = [a for a in args if a.isalnum()]
    result = subprocess.run([cmd, *clean_args], capture_output=True, text=True, check=True)
    return result.stdout

# --- 5) Safe (de)serialization ---
# Avoid pickle for untrusted data; use JSON or your own schema validation
import json

def parse_user_input(json_str: str):
    data = json.loads(json_str)
    # minimal schema check
    if not isinstance(data, dict) or "name" not in data:
        raise ValueError("Invalid input schema.")
    return data["name"]

# --- Example usage ---
if _name_ == "_main_":
    # Create a demo DB
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        conn.execute("INSERT OR IGNORE INTO users(name) VALUES (?)", ("alice",))
        print(get_user_by_name(conn, "alice"))

    saved = save_user_file("hello.txt", b"safe write")
    print("Saved:", saved)

    print(run_tool("echo", "Hello123"))