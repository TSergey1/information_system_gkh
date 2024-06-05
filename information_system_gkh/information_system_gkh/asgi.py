import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'information_system_gkh.settings')

application = get_asgi_application()
