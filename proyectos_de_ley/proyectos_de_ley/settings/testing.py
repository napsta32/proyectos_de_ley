from .base import *
import sys


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
print(TESTING)
