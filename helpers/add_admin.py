from helpers.base import *

from apps.users.models import User
User.objects.create_superuser(email='admin', password='root')
