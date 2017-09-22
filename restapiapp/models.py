from django.db import models


USER_STATES = (('active', 'active'), ('inactive', 'inactive'))


class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    status = models.CharField(choices=USER_STATES, max_length=100, default='inactive')
