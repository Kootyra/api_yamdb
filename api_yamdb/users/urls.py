from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('auth/signup/', views.UserRegistration.as_view({'post': 'signup'}), name='signup'),
    path('auth/token/', views.UserConfirmation.as_view({'post': 'confirmation'}), name='token_obtain_pair'),
    path('users/me/', views.UserProfile.as_view({'patch': 'profile'})),
] 
