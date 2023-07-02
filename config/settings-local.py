from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# sqlite3 database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}