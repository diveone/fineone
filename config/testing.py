import os

TESTING = True
DATABASE = 'finone_test'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'finone_test'

# Modify for custom settings
DB_USER = os.getenv('DB_USER', 'proto')
DB_PWD = os.getenv('DB_PASSWORD', 'admin')
