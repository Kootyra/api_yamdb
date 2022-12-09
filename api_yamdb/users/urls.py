from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', views.UserProfile, basename='users')

urlpatterns = [
    path('auth/signup/',
         views.UserRegistration.as_view({'post': 'signup'}),
         name='signup'),
    path('auth/token/',
         views.UserConfirmation.as_view({'post': 'confirmation'}),
         name='token'),
    path('', include(router.urls))
]
