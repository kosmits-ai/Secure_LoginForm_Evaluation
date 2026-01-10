from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",   # Good baseline
    SESSION_COOKIE_SECURE=False      # Set True only when you run HTTPS
)

def get_db():
    connection = sqlite3.connect('login.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]

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


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template("dashboard.html", username=session["username"], mode="SAFE", csrf_token = get_csrf_token())

@app.route("/dashboard/update_status", methods=["POST"])
def update_status():
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized"}), 401
    token = request.form.get("csrf_token", "")
    if token != session.get("csrf_token"):
        return "CSRF validation failed", 403

    status = request.form.get("status", "")
    session["status"] = status  # Store status in server-side session
    

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))   #server-side session data cleared on logout

if __name__ == "__main__":
    app.run(debug=False)
