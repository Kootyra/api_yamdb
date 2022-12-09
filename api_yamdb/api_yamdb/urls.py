from django.urls import include, path
from django.views.generic import TemplateView
from api.views import CommentViewSet, ReviewViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('api.urls')),
    path('api/v1/', include('users.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
