from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product  # غير Product باسم الموديل بتاعك لو مختلف

# مثال: تنفيذ شيء قبل الحفظ
@receiver(pre_save, sender=Product)
def prevent_duplicate_model_registration(sender, instance, **kwargs):
    # هذا مثال آمن، ممكن تحذف أو تعدل حسب حاجتك
    pass
