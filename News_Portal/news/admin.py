from django.contrib import admin
from .models import Category, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'authorship', 'publication_time')
    list_filter = ('title', 'authorship', 'publication_time')
    search_fields = ('title', 'category__title')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
