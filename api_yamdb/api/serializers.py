import logging
import re

from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers

from reviews.models import Category, Genre, Title

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filename='mylog.log',
    filemode='w'
)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ['id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category']


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True)

    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug')


    class Meta:
        model = Title
        fields = '__all__'


    # def to_representation(self, value):
    #     logging.debug(self)
    #     pass


class TitlePostSerializer(TitleGetSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True)
