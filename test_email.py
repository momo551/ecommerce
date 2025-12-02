import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

# Test email sending
try:
    send_mail(
        'Test Subject',
        'Test message body.',
        settings.DEFAULT_FROM_EMAIL,
        ['admin@gmail.com'],  # Replace with your test email
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
