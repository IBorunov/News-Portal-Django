from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_rating = Post.objects.filter(authorship=self).aggregate(author_post_rating=Coalesce(Sum('rating'), 0))['author_post_rating']
        author_comment_rating = Comment.objects.filter(user=self.user).aggregate(author_comment_rating=Coalesce(Sum('rating'), 0))['author_comment_rating']
        user_comment_rating = Comment.objects.filter(post__authorship=self).aggregate(user_comment_rating=Coalesce(Sum('rating'), 0))['user_comment_rating']
        self.rating = author_post_rating * 3 + author_comment_rating + user_comment_rating
        self.save()

    def __str__(self):
        return self.user.username
class Category(models.Model):
    name = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return self.name

class Post(models.Model):

    article = 'A'
    news = 'N'
    CHOISE = [
        (article, 'статья'),
        (news, 'новость')
    ]

    authorship = models.ForeignKey(Author, on_delete = models.CASCADE)
    type = models.CharField(max_length=1, choices=CHOISE, default=news)
    publication_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='Post_Category')
    title = models.CharField(default='Здесь должен быть заголовок', max_length=225)
    text = models.TextField(default='Здесь должен быть текст')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Post_Category(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Здесь должен быть текст')
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()


