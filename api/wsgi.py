import os
import sys
from pathlib import Path

# إضافة مشروع Django إلى sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ضبط settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# استدعاء Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
