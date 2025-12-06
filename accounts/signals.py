# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    هذا الـ signal ينشئ Profile تلقائيًا لكل مستخدم جديد.
    """
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    هذا الـ signal يحفظ الـ Profile بعد حفظ الـ User.
    تأكد من وجود الـ profile قبل الحفظ لتجنب أي خطأ.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
