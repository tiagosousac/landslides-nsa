from flask import render_template
from app import app
from app.exporter import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')