from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post_Category
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'emails/post_created_email.html', {
            'text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=Post_Category)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails +=[s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)