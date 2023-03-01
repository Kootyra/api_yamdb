import logging
import re

from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers

from reviews.models import Category, Genre, Title, Review, Comment

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


class GenreTitleField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return value.genre.values('name', 'slug')

    def to_internal_value(self, data):
        return Genre.objects.filter(slug__regex='|'.join(data))


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True)

    genre = GenreTitleField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'review')
        model = Comment
