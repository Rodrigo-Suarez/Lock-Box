from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('LOCAL_DB_NAME'),
        'USER': os.environ.get('LOCAL_DB_USER'),
        'PASSWORD': os.environ.get('LOCAL_DB_PASSWORD'),
        'HOST': os.environ.get('LOCAL_DB_HOST'),
        'PORT': os.environ.get('LOCAL_DB_PORT')
    }
}

# Renderizadores adicionales para desarrollo
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
    'rest_framework.renderers.BrowsableAPIRenderer',
)


#TOKEN
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
