import os
import sys

# مسار مشروعك على PythonAnywhere
project_home = '/home/mohamedelzafar/ecommerce'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ضبط settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# استدعاء Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(application)