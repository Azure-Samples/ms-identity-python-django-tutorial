from .settings import *
ALLOWED_HOSTS = ['*']
DEBUG = False
# USE_X_FORWARDED_HOST = True # this is so that HTTPS scheme is generated for request.get_absolute_uri (Azure is reverse proxy, Django thinks it is HTTP traffic even when actually HTTPS)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # this is so that HTTPS scheme is generated for request.get_absolute_uri (Azure is reverse proxy, Django thinks it is HTTP traffic even when actually HTTPS)

print("USING AZURE SETTINGS.")

DEBUG = False
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('APP_DB_NAME'),
        'USER': '{}@{}'.format(os.getenv('POSTGRES_ADMIN_USER'), os.getenv('POSTGRES_SERVER_NAME')),
        'PASSWORD': os.getenv('POSTGRES_ADMIN_PASSWORD'),
        'HOST': os.getenv('POSTGRES_FULLY_QUALIFIED_DOMAIN_NAME'),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}
