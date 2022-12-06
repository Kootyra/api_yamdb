from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import CommentViewSet, ReviewViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'review', ReviewViewSet)
router.register(r'review/(?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include('users.urls'))
]
