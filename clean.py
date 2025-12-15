import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

from products.models import Product

for product in Product.objects.all():
    if product.image:
        url = str(product.image)
        # إزالة أي /media/ قبل رابط Cloudinary
        if url.startswith("/media/https://") or url.startswith("/media/https%3A"):
            clean_url = url.replace("/media/", "")
            product.image = clean_url
            product.save()
            print(f"[CLEANED] {product.name} → {clean_url}")
