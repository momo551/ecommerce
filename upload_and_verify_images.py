import os
import django
from django.core.files.base import ContentFile
import requests

# -------------------------
# إعداد Django
# -------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

# -------------------------
# استدعاء الموديل
# -------------------------
from products.models import Product
from django.conf import settings
from django.core.files.storage import default_storage

# -------------------------
# مسار الصور المحلية
# -------------------------
MEDIA_PRODUCTS_PATH = os.path.join(settings.MEDIA_ROOT, 'products')
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']

# -------------------------
# تنظيف URLs المشوهة
# -------------------------
print("=== Cleaning malformed image URLs ===")
for product in Product.objects.all():
    if product.image and product.image.url.startswith("/media/https://"):
        product.image = None
        product.save()
        print(f"[RESET] {product.name} → Image URL reset")

# -------------------------
# رفع الصور الموجودة محليًا
# -------------------------
print("\n=== Uploading local images to Cloudinary ===")
for product in Product.objects.all():
    # الحصول على اسم الملف المحلي
    local_file = None
    if product.image:
        # استخدم اسم الملف الحالي إذا موجود
        local_file = os.path.join(MEDIA_PRODUCTS_PATH, os.path.basename(product.image.name))
        if not os.path.isfile(local_file):
            local_file = None

    if not local_file:
        # حاول إيجاد الملف المحلي بناءً على اسم المنتج
        safe_name_base = product.name.replace(" ", "_")
        for ext in ALLOWED_EXTENSIONS:
            candidate_path = os.path.join(MEDIA_PRODUCTS_PATH, safe_name_base + ext)
            if os.path.isfile(candidate_path):
                local_file = candidate_path
                break

    if local_file:
        try:
            filename = os.path.basename(local_file)
            with open(local_file, "rb") as f:
                product.image.save(
                    filename,
                    ContentFile(f.read()),
                    save=True
                )
            print(f"[UPLOADED] {product.name} → {filename}")
        except Exception as e:
            print(f"[ERROR] {product.name} → {e}")
    else:
        print(f"[MISSING] {product.name} → No local file found")

# -------------------------
# تحقق بعد الرفع على Cloudinary
# -------------------------
print("\n=== Verifying uploaded images on Cloudinary ===")
for product in Product.objects.all():
    if product.image:
        # URL النهائي بعد الحفظ
        image_url = product.image.url
        if image_url.startswith("http://") or image_url.startswith("https://"):
            try:
                response = requests.head(image_url)
                if response.status_code == 200:
                    print(f"[OK] {product.name} → Cloudinary image exists: {image_url}")
                else:
                    print(f"[MISSING] {product.name} → Cloudinary image NOT found: {image_url}")
            except Exception as e:
                print(f"[ERROR] {product.name} → Error checking image: {e}")
        else:
            print(f"[ERROR] {product.name} → URL is relative (should be absolute): {image_url}")
    else:
        print(f"[MISSING] {product.name} → No image assigned")
