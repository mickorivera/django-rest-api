from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'