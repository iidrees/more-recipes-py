import os

import requests
import operator
import re
import nltk
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from worker import conn, count_and_save_words
from flask import jsonify

import config
import settings


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    
    if request.method == "POST":
        # get url that the user has entered
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url
        
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print(job.get_id())
    return render_template('index.html', results=results)


@app.route('/results/<job_key>', methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)
    # return str(job.result), 200
    print(">>>>>>>>>", job)

    if job.is_finished:
        # return str(job.result), 200
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202

if __name__ == '__main__':
    app.run()
