# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vinge_dev',
        'USER': 'vinge',
        'PASSWORD': '',
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
