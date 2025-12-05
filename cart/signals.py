from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart  # تأكد إن عندك موديل Cart

# مثال: كل مرة بيتعمل فيها Cart جديد
@receiver(post_save, sender=Cart)
def cart_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new cart has been created: {instance}")
