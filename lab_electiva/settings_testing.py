SECRET_KEY = 'bs8szt@qtn3=)$*o#tuq(nf9*4^b7v508+b!i4'
from .settings import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':'memory',
    }
}