from django.apps import AppConfig

class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        # استدعاء signals هنا بدل ما يكون في أعلى الملفات
        # ده يحميك من مشكلة إعادة تسجيل الموديلات عند إعادة التحميل
        try:
            import cart.signals  # لو عندك ملف signals في تطبيق cart
        except ImportError:
            pass
