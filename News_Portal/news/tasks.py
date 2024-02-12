import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Category

@shared_task
def notify_subscribers(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
        'emails/post_created_email.html', {
            'text': post.preview(),
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(subject=post.title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers_emails)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def weekly_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(publication_time__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'emails/weekly_posts_email.html',
        {'link': settings.SITE_URL,
         'posts' : posts}
    )
    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
