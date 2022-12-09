from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]

    username = models.CharField(
        blank=False,
        null=False,
        max_length=250,
        unique=True
    )
    email = models.EmailField(
        blank=False,
        null=False,
        max_length=254,
        unique=True)

    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='user',
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
