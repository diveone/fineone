import logging, os
# from .common import *


DEBUG = True

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = os.getenv('DB_FINONE')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PASSWORD')

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_NAME)
LOCAL_ENDPOINT = "http://localhost:3333/test"
# Modify for custom settings
