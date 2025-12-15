import os
import re
import urllib.parse
from decouple import config
import cloudinary
import cloudinary.uploader
import django

# إعداد Django للوصول للـ ORM خارج manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from products.models import Product

# إعداد Cloudinary
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

MEDIA_PRODUCTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'products')

def normalize_name(name):
    # تحويل الاسم لحروف صغيرة، الفراغات لـ _، وحذف الرموز الخاصة
    name = name.lower()
    name = re.sub(r'[%()\[\]\-]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name

def find_matching_file(product_name):
    normalized = normalize_name(product_name)
    for filename in os.listdir(MEDIA_PRODUCTS_DIR):
        file_normalized = normalize_name(os.path.splitext(filename)[0])
        if file_normalized == normalized:
            return os.path.join(MEDIA_PRODUCTS_DIR, filename)
    return None

def reset_relative_urls():
    print("=== Resetting old Cloudinary URLs ===")
    for product in Product.objects.all():
        if product.image and not str(product.image).startswith("http"):
            print(f"[RESET RELATIVE] {product.name} → {product.image}")
            product.image = None
            product.save()

def upload_local_images():
    print("\n=== Uploading local images to Cloudinary ===")
    for product in Product.objects.all():
        if product.image and str(product.image).startswith("http"):
            continue  # الصورة موجودة على Cloudinary بالفعل

        local_file = find_matching_file(product.name)
        if local_file:
            try:
                res = cloudinary.uploader.upload(local_file, folder="products")
                product.image = res['secure_url']
                product.save()
                print(f"[UPLOADED] {product.name} → {product.image}")
            except Exception as e:
                print(f"[ERROR] {product.name} → {e}")
        else:
            print(f"[MISSING FILE] {product.name} → No matching local image found")

def verify_images():
    print("\n=== Verifying images ===")
    for product in Product.objects.all():
        if product.image:
            url = str(product.image)
            if url.startswith("http"):
                print(f"[OK] {product.name} → {url}")
            else:
                print(f"[ERROR] {product.name} → URL is relative or missing: {url}")
        else:
            print(f"[MISSING] {product.name} → No image assigned")

if __name__ == "__main__":
    reset_relative_urls()
    upload_local_images()
    verify_images()
