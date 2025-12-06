import os
import django
from django.test import Client
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

# Test the home page
client = Client()
response = client.get('/')
print(f"Home page status: {response.status_code}")
if response.status_code == 200:
    print("✅ Home page is working!")
else:
    print("❌ Home page still has issues")
    print(f"Response content: {response.content[:500]}")
