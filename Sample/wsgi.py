"""
WSGI config for Sample project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# if there is no environment set, use local environment values
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sample.settings')

application = get_wsgi_application()
