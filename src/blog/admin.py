from django.contrib import admin
from .models import Post, Comment, Image, Category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Category)
