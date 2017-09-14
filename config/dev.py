from .common import *


DEBUG = True

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_FINONE', 'finone_dev')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PWD = os.getenv('DB_PASSWORD', 'admin')

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_NAME)
LOCAL_ENDPOINT = "http://localhost:3333/test"
# Modify for custom settings
