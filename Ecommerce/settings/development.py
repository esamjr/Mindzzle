from Ecommerce.settings.base import *
import environ

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env('./.env')

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost',
]

DATABASES = {}
DATABASE_URL = env('DB_URL')
DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=None)
