# Project Rename Plan: fashion_site → ecommerce

## Steps to Complete:

- [x] Rename 'fashion_site' directory to 'ecommerce'
- [x] Update fashion_site/settings.py → ecommerce/settings.py (references to 'fashion_site')
- [x] Update fashion_site/urls.py → ecommerce/urls.py (references to 'fashion_site')
- [x] Update fashion_site/wsgi.py → ecommerce/wsgi.py (references to 'fashion_site')
- [x] Update fashion_site/asgi.py → ecommerce/asgi.py (references to 'fashion_site')
- [x] Update templates/base.html (change 'Fashion Site' to 'E-commerce')
- [x] Update Procfile (change 'fashion_site' to 'ecommerce')
- [x] Update vercel.json (change 'fashion_site' to 'ecommerce') - No change needed, uses api
- [x] Update manage.py (change DJANGO_SETTINGS_MODULE if needed) - No change needed, uses api.settings
- [ ] Run python manage.py makemigrations and migrate
- [ ] Test the application
