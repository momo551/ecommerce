# Example placeholder for future signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order  # تأكد إن عندك موديل Order

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new order was created: {instance}")
