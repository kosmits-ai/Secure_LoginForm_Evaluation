import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect('login.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

username = 'admin'
password = generate_password_hash('password')

cursor.execute(
    "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    (username, password)
)


connection.commit()
connection.close()

print("Database initialized with default user.")
