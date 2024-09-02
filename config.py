from flask import Flask,  render_template
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
import logging
import os

app = Flask(__name__, template_folder='templates') 
app.url_map.strict_slashes = False
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('postgres://u63krlnclqemjd:peb1fe8889ba5f449883feba1fc4a11d8b7f7c9ce5407faa0dc476ba30d014d08@c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d58gfiaefviqgf', 'sqlite:///mydatabase.db')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')