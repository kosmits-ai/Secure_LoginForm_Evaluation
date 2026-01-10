from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect('login.db')
    connection.row_factory = sqlite3.Row
    return connection

# Render login page
@app.route("/")
def index():
    return render_template("index.html")

# REST API endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    #cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")   #this would be vulnerable to SQL injection

    user = cursor.fetchone()
    connection.close()

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    return jsonify({"message": "Login successful"}), 200

    

@app.route("/crash")
def crash():
    return 1 / 0

if __name__ == "__main__":
    app.run(debug=True)
