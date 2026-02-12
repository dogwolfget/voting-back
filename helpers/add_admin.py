import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
import django
django.setup()

from apps.users.models import User
User.objects.create_superuser(email='admin', password='root')
