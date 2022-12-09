import logging
import re

from django.shortcuts import get_object_or_404
# from django_filters import rest_framework as djfilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reviews.models import Category, Genre, Title

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer)

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


# class TitleFilter(djfilters.FilterSet):
#     genre = djfilters.CharFilter()
#     category = djfilters.CharFilter()
#
#     class Meta:
#         model = Title
#         fields = ['name',
#                   'year',]

class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleGetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # filterset_class = TitleFilter
    # ordering_fields = ['name',
    #                    'year',
    #                    'genre',
    #                    'category']
    filterset_fields = ['name',
                        'year',
                        'genre',
                        'category',]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        logging.debug(self)
        return Title.objects.all()
