import datetime
import re
import sqlite3
from flask import Flask, redirect
from markupsafe import escape
from flask import render_template
from flask import request,jsonify
from flask_cors import CORS
import sqlite3, jwt, datetime
from passlib.hash import bcrypt
app = Flask(__name__)

CORS(app)  # allow frontend requests

SECRET = "mysecret"
ALGORITHM = "HS256"

# --- Database setup ---
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT UNIQUE,
    experience TEXT,
    timeCommitment TEXT,
    password TEXT
)""")
conn.commit()

@app.route('/n')
def n():
    return '<marquee>Welcome to Flask!</marquee>'
@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', person=name)
@app.route('/signup')
def signup():
    return render_template('getstarted.html')

@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    experience = data.get("experience")
    timeCommitment = data.get("timeCommitment")
    password = "NAVNEET"
    if not email or not password or not firstName or not lastName or not experience or not timeCommitment:
        return jsonify({"error": "All fields are required"}), 400
    hashed = bcrypt.hash(password)
    try:
        cur.execute("INSERT INTO users (firstName, lastName, email, experience, timeCommitment, password) VALUES (?, ?, ?, ?, ?, ?)", 
                    (firstName, lastName, email, experience, timeCommitment, hashed))
        conn.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 400
@app.route('/signin')
def signin():
    return render_template('login.html')
    
# --- Login route ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE email=?", (email,))
        row = cur.fetchone()
        if not row or not bcrypt.verify(password, row[0]):
            return jsonify({"error": "Invalid credentials"}), 401

        token = jwt.encode(
            {"email": email, "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)},
            SECRET,
            algorithm=ALGORITHM
        )
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return jsonify({"token": token})

@app.route('/api/dashboard', methods=["GET"])
def api_dashboard():
    auth_header= request.headers.get('Authorization')
    print("Authorization Header:", auth_header)
    if not auth_header or not auth_header.startswith("Bearer "):        
        return jsonify({"error": "Authorization header missing"}), 401
    token = auth_header.split(" ")[1]
    try:
        decode = jwt.decode(token, SECRET, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401   


@app.route('/dashboard/<token>')
def dashboard(token):
    decode=jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    if not decode:
        return redirect('/signin')
    return render_template('UserDashboard.html',email=decode['email'],)
if __name__ == '__main__':
    app.run(debug=True)  # Set debug to True for development purposes
debug = True