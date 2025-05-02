import datetime
import re
from flask import Flask
from markupsafe import escape
from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', person=name)


debug = True