import logging

from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as djfilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, Review, Comment

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          ReviewSerializer, CommentSerializer)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filename='mylog.log',
    filemode='w',
)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        if (len(self.kwargs) != 0 and
            (self.request.method == 'GET' or
            self.request.method == 'PATCH')):
            raise MethodNotAllowed(self.request.method)
        return Category.objects.all()

    def destroy(self, request, **kwargs):
        instance = get_object_or_404(Category, slug=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        if (len(self.kwargs) != 0 and
            (self.request.method == 'GET' or
            self.request.method == 'PATCH')):
                raise MethodNotAllowed(self.request.method)
        return Genre.objects.all()

    def destroy(self, request, **kwargs):
        instance = get_object_or_404(Genre, slug=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleFilter(djfilters.FilterSet):
    name = djfilters.CharFilter(field_name='name', lookup_expr='contains')
    genre = djfilters.CharFilter(field_name='genre', lookup_expr='slug')
    category = djfilters.CharFilter(field_name='category', lookup_expr='slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_class = TitleFilter
    ordering = ['-id']


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset
