from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "vulnerable_app_secret_key"


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
    data = request.get_json(silent=True) or {} # Handle missing or invalid JSON to protect from debug = True in app.run

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
    
    session['user_id'] = user["id"]
    session["username"] = user["username"]
    
    return jsonify({"message": "Login successful"}), 200

@app.route("/dashboard_vuln")
def dashboard_vuln():
    # Missing authorization check!
    # Anyone can open /dashboard_vuln without logging in.
    username = session.get("username")  # might be None
    return render_template("dashboard.html", username=username, mode="VULNERABLE")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template("dashboard.html", username=session["username"], mode="SAFE")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))   #server-side session data cleared on logout

if __name__ == "__main__":
    app.run(debug=True)
