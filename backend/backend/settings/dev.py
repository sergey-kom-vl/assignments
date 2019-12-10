ALLOWED_HOSTS = '127.0.0.1', 'localhost',

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'assignments',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': '192.168.220.130',
        'PORT': '5432',
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': '192.168.220.130',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'pass',
        'DEFAULT_TIMEOUT': 360,
    },
}

WKHTMLTOPDF_URL = 'http://192.168.220.130:8080/'
