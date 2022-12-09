from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls))
]
