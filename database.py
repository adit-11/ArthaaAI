import sqlite3
import hashlib

DB_NAME = "fintech.db"

# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- USER TABLE ----------------
def create_user_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- PASSWORD HASHING ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- REGISTER USER ----------------
def register_user_db(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# ---------------- AUTHENTICATE USER ----------------
def authenticate_user_db(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    return result[0] == hash_password(password)


# ---------------- INSERT TRANSACTION ----------------
def insert_transaction(username, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (username, amount) VALUES (?, ?)",
        (username, amount)
    )

    conn.commit()
    conn.close()


# ---------------- GET USER TRANSACTIONS ----------------
def get_user_transactions(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM transactions WHERE username = ?",
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]