from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ForeignKey('Image', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)
    live = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.SlugField(null=True, blank=True)
    text = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
