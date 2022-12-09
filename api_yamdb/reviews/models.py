from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CHARS_IN_RETURN = 100


class Category(models.Model):
    name = models.CharField(verbose_name='Название группы ',
                            max_length=256,
                            unique=True)
    slug = models.SlugField(verbose_name='Адрес для ссылки',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Название жанра',
                            max_length=256,
                            unique=True)
    slug = models.SlugField(verbose_name='Адрес для ссылки',
                            max_length=50,
                            unique=True)
    title = models.ManyToManyField(
        'Title',
        through='GenreTitle',
        related_name='genre',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(verbose_name='Год',)
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='title')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text[:CHARS_IN_RETURN]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
