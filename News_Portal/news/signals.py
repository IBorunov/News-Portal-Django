from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post_Category
from .tasks import notify_subscribers


@receiver(m2m_changed, sender=Post_Category)
def notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        notify_subscribers.delay(instance.pk)



