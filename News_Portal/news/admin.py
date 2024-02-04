from django.contrib import admin
from .models import Category, Post, Post_Category


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Post_Category)