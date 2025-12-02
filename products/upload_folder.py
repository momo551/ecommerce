import os
import django
import cloudinary
import cloudinary.uploader

# تهيئة Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

from products.models import Product
from django.db.models import Q

# إعداد Cloudinary من environment variables
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# مسار المجلد اللي فيه الصور
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_path = os.path.join(BASE_DIR, "media/products_to_upload")

# جلب كل الملفات في المجلد
images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# رفع كل صورة وتحديث الموديل
for image in images:
    image_path = os.path.join(folder_path, image)
    public_id = os.path.splitext(image)[0]  # الاسم بدون امتداد

    # رفع الصورة على Cloudinary
    result = cloudinary.uploader.upload(
        image_path,
        public_id=public_id
    )
    secure_url = result['secure_url']
    print(f"Uploaded {image}: {secure_url}")

    # تحديث الرابط في قاعدة البيانات
    try:
        # البحث عن المنتج بالاسم أو بالـ slug (لو موجود)
        product = Product.objects.filter(Q(name__iexact=public_id) | Q(slug__iexact=public_id)).first()
        if product:
            product.image = secure_url  # افترض أن الحقل اسمه image
            product.save()
            print(f"Updated Product {product.name} with new image.")
        else:
            print(f"No product found for {public_id}, skipping.")
    except Exception as e:
        print(f"Error updating product for {public_id}: {e}")
