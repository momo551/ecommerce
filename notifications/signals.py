# Example placeholder for future signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification  # تأكد إن عندك موديل Notification

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new notification was created: {instance}")
