import os
import sys

# إضافة مسار المشروع
project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ضبط settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

# استدعاء ASGI application
from django.core.asgi import get_asgi_application
application = get_asgi_application()
