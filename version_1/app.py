from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

    if username != "admin":
        return jsonify({"message": "User does not exist"}), 404

    if password != "password":
        return jsonify({"message": "Wrong password"}), 401

    return jsonify({"message": "Login successful"}), 200

@app.route("/crash")
def crash():
    return 1 / 0

if __name__ == "__main__":
    app.run(debug=True)
