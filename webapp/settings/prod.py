from .common import *


STATIC_ROOT = "/var/webapp/static/"
MEDIA_ROOT = '/var/webapp/media/'

DATABASES = {
    'default': {
        'HOST': 'webapp-db',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'bidonow',
        'NAME': 'bidonow',
    }
}
