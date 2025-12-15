import os
import shutil

# المسار الأصلي للفولدر اللي فيه الصور
SOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products')

# المسار الجديد تحت media/products/
DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'products')

# إنشاء الفولدر لو مش موجود
os.makedirs(DEST_DIR, exist_ok=True)

# نسخ كل ملفات الصور من المصدر للوجهة
for filename in os.listdir(SOURCE_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(DEST_DIR, filename)
        shutil.copy2(src_path, dest_path)
        print(f"[COPIED] {filename} → media/products/")
print("=== Image files moved to media/products/ ===")