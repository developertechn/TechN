import datetime
import re
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
import db
app = Flask(__name__)

@app.route('/n')
def n():
    return '<marquee>Welcome to Flask!</marquee>'
@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', person=name)
@app.route('/signup')
def signup():
    return render_template('RegisterUser.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        # Validate input
        if not username or not password or not email or not mobile:
            error = "All fields are required!"
        else:
            res=db.register_user(username, email, mobile, password)
            if not res:
                error = "Registration failed. Please try again."
            else:
                # Registration successful
                return f"Registered successfully as {escape(username)} with Response: {escape(res)}"
        # Perform signup logic here

        return f"Signed up as {escape(username)} with Response: {escape(res)}"
    return render_template('signup.html', error=error)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error= None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Perform login logic here
        return f"Logged in as {escape(username)}"
    return render_template('login.html',error=re.error)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # Perform file upload logic here
        file.save(f"uploads/{file.filename}")
        # Save the file to a directory named 'uploads'
        return f"File {escape(file.filename)} uploaded successfully!"
    return render_template('upload.html')
debug = True