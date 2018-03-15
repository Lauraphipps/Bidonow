print('Load settings.dev')
from .common import *

STATIC_ROOT = None  # defined in local_settings
MEDIA_ROOT = None  # defined in local_settings

DATABASES = None  # defined in local_settings

try:
    from .local_settings import *
except ImportError:
    pass
