import os

INSTANCE_TYPE = os.environ.get('INSTANCE_TYPE', 'dev') # can be 'dev' or 'prod'
print('INSTANCE_TYPE={}'.format(INSTANCE_TYPE))


if INSTANCE_TYPE not in ('dev', 'prod'):
    raise Exception('INSTANCE_TYPE can be only "dev" or "prod"')


if INSTANCE_TYPE == 'dev':
    try:
        from .dev import *
    except ImportError:
        pass


if INSTANCE_TYPE == 'prod':
    try:
        from .prod import *
    except ImportError:
        pass
