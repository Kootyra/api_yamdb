import logging

from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

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
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title, id=self.context.get('view').kwargs.get('title_id')
        )
        author = request.user
        if request.method == 'POST' and Review.objects.filter(
                author=author, title=title).exists():
            raise ValidationError('you already have posted review')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'review')
        model = Comment
