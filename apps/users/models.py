from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin as PermissionsModel,
)
from django.db import models

from apps.core.models import TimestampModel
from apps.users.managers import UserManager


class User(PermissionsModel, TimestampModel, AbstractBaseUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'

    objects = UserManager()

    email = models.EmailField(verbose_name='Email', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email
