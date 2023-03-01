from django.contrib import admin

from .models import ConfCode, User

admin.site.register(User)

admin.site.register(ConfCode)
