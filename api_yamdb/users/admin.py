from django.contrib import admin

from .models import User, ConfCode

admin.site.register(User)

admin.site.register(ConfCode)