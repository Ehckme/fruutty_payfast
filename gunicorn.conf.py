import multiprocessing
from os import environ


bind = '127.0.0.1:' + environ.get('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = 1
