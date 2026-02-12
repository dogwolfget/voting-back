from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def __create_user(
        self,
        email,
        password=None,
        is_active=False,
        is_staff=False,
        is_superuser=False,
    ):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **kwargs):
        return self.__create_user(
            email,
            password,
            is_active=kwargs.get('is_active', False),
            is_staff=kwargs.get('is_staff', False),
            is_superuser=kwargs.get('is_superuser', False),
        )

    def create_superuser(self, email, password):
        return self.__create_user(
            email,
            password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
