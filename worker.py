import os

import redis
from rq import Worker, Queue, Connection

# import app

from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup

import re
import nltk
import requests

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)



def count_and_save_words(url):
    errors = []

    print(">>>>>>>> URL>>>>>>", url)
    try:
        r = requests.get(url)
        print(">>><><><><><><><THE RRRRRR<><><><><>",r)

    except:
        errors.append("Unable to get URL. Please make sure it's valid and try again.")
        return {"error": errors}
    
    # Text processing
    raw = BeautifulSoup(r.text).get_text()
    nltk.data.path.append('./nltk_data/') # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
        