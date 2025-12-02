from django.core.mail import send_mail
from django.conf import settings

def send_purchase_notification(order):
    """
    Send an email notification to the admin when a purchase is made.
    """
    subject = f'New Purchase Notification - Order #{order.id}'
    message = f"""
    A new purchase has been made.

    Customer Details:
    - Name: {order.first_name} {order.last_name}
    - Email: {order.email}
    - Address: {order.address}, {order.city}, {order.postal_code}

    Order Details:
    - Order ID: {order.id}
    - Total Cost: ${order.get_total_cost()}
    - Products:
    """
    for item in order.items.all():
        message += f"  - {item.product.name} (Quantity: {item.quantity}, Price: ${item.price})\n"

    message += f"\nOrder Date: {order.created}"

    # Send email to admin
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['momo55265526@gmail.com'],  # Admin email address
        fail_silently=False,
    )
