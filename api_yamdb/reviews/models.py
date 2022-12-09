from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='title')
    genre = models.ManyToManyField(
        'Genre',
        related_name='title')

    def __str__(self):
        return self.name
