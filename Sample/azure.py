from .settings import *
ALLOWED_HOSTS = ['*']
DEBUG = False
USE_X_FORWARDED_HOST = True # this is so that HTTPS scheme is generated for request.get_absolute_uri (Azure is reverse proxy, Django thinks it is HTTP traffic even when actually HTTPS)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # this is so that HTTPS scheme is generated for request.get_absolute_uri (Azure is reverse proxy, Django thinks it is HTTP traffic even when actually HTTPS)


print("USING AZURE SETTINGS.")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('APP_DB_NAME'),
        'USER': '{}@{}'.format(os.getenv('POSTGRES_ADMIN_USER'), os.getenv('POSTGRES_SERVER_NAME')),
        'PASSWORD': os.getenv('POSTGRES_ADMIN_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}
