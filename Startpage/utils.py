import requests
from rq import Queue
from worker import conn

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

if __name__ == '__main__':
  q = Queue(connection=conn)
  result = q.enqueue(count_words_at_url, 'http://heroku.com')
