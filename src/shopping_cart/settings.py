import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# General stuff
PROJECT_NAME = 'shopping_cart'
API_STR = ''

# CORS
BACKEND_CORS_ORIGINS = []

# Super-user
FIRST_SUPERUSER = os.environ.get('FIRST_SUPERUSER')
FIRST_SUPERUSER_PASSWORD = os.environ.get('FIRST_SUPERUSER_PASSWORD')

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# security
ACCESS_TOKEN_EXPIRE_MINUTES = 10
SECRET_KEY = os.environ.get('SECRET_KEY')
