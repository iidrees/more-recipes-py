import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config
import settings


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from models import Result

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/<name>')
def hello_name(name):
    return 'Hello {}'.format(name)

if __name__ == '__main__':
    app.run()
