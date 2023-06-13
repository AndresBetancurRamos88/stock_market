import secrets

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def get_key(self):
        return secrets.token_hex(15)

    def _create_user(
        self,
        name: str,
        last_name: str,
        email: str,
        is_staff: bool,
        is_superuser: bool,
        password: str,
        **extra_fields,
    ):
        user = self.model(
            name=name,
            last_name=last_name,
            email=email,
            key=self.get_key(),
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self, name, last_name, email, password=None, **extra_fields
    ):
        return self._create_user(
            name, last_name, email, False, False, password, **extra_fields
        )

    def create_superuser(
        self, name, last_name, email, password=None, **extra_fields
    ):
        return self._create_user(
            name, last_name, email, True, True, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    key = models.CharField(unique=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "last_name"]

    def __str__(self) -> str:
        return f"{self.email}"
