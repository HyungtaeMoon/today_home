from .base import *
secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# WSGI
WSGI_APPLICATION = 'config.wsgi.dev.application'

# DB
DATABASES = secrets['DATABASES']

# django-storages
INSTALLED_APPS += [
    'storages',
]

# Media
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
