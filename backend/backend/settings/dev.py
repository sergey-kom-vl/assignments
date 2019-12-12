ALLOWED_HOSTS = '127.0.0.1', 'localhost',
DOCKER_HOST = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'assignments',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': DOCKER_HOST,
        'PORT': '5432',
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': DOCKER_HOST,
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'pass',
        'DEFAULT_TIMEOUT': 360,
    },
}

HTML2PDF_URL = f'http://{DOCKER_HOST}:8080'
