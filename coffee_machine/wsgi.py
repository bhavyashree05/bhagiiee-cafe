"""
WSGI config for coffee_machine project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffee_machine.settings")

application = get_wsgi_application()
