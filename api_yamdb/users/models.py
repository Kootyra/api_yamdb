from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        null=False,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True,
)

class ConfCode(models.Model):
    confirmation_code = models.CharField(verbose_name='Код подтверждения',
                             max_length=10)
    username = models.ForeignKey(
        User,
        verbose_name='Имя пользователя',
        on_delete=models.CASCADE,
    )