from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserConfirmation, UserProfile,
                    UserRegistration)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', UserProfile, basename='users')

urlpatterns = [
    path('auth/signup/',
         UserRegistration.as_view({'post': 'signup'}),
         name='signup'),
    path('auth/token/',
         UserConfirmation.as_view({'post': 'confirmation'}),
         name='token'),
    path('', include(router.urls))
]
