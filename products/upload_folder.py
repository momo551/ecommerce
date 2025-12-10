import os
import sys
import django
import cloudinary
import cloudinary.uploader
import difflib
import urllib.parse  # مهم للتعامل مع المسافات والرموز الخاصة
from decouple import config

# تهيئة Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

from products.models import Product

# إعداد Cloudinary
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

# مسار المجلد اللي فيه الصور
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_path = os.path.join(BASE_DIR, "media/products_to_upload")

# جلب كل الملفات في المجلد
images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# جلب كل أسماء المنتجات
products = list(Product.objects.all())
product_names = [p.name for p in products]

for image in images:
    image_path = os.path.join(folder_path, image)
    file_name = image.split('.')[0].replace("_", " ").lower()

    # البحث عن أقرب اسم منتج باستخدام difflib
    match_name = difflib.get_close_matches(file_name, product_names, n=1, cutoff=0.4)
    if not match_name:
        print(f"No good match for {image}, skipping.")
        continue

    match_name = match_name[0]  # أقرب تطابق
    product = Product.objects.get(name=match_name)

    # حذف الصورة القديمة إذا كانت موجودة على Cloudinary
    if product.image and hasattr(product.image, 'url') and product.image.url.startswith("http"):
        # استخراج public_id بطريقة آمنة
        public_id_old = os.path.splitext(os.path.basename(urllib.parse.unquote(product.image.url)))[0]
        try:
            cloudinary.uploader.destroy(public_id_old)
            print(f"Deleted old image for {product.name}: {public_id_old}")
        except Exception as e:
            print(f"Failed to delete old image for {product.name}: {e}")

    # رفع الصورة الجديدة على Cloudinary
    # استبدال الفراغات بشرطة سفلية لتجنب مشاكل في public_id
    safe_public_id = file_name.replace(" ", "_")
    result = cloudinary.uploader.upload(image_path, public_id=safe_public_id)
    secure_url = result['secure_url']
    print(f"Uploaded {image}: {secure_url}")

    # تحديث الرابط في قاعدة البيانات
    product.image = secure_url
    product.save()
    print(f"Updated Product {product.name} with new image.")
