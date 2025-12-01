from django.test import TestCase
from django.core import mail
from notifications.utils import send_purchase_notification
from orders.models import Order, OrderItem
from products.models import Product, Category
from django.contrib.auth.models import User


class NotificationTestCase(TestCase):
    def test_send_purchase_notification(self):
        # Create a user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create a category
        category = Category.objects.create(name='Test Category', slug='test-category')

        # Create a product
        product = Product.objects.create(name='Test Product', slug='test-product', description='Test Description', price=10.00, category=category)

        # Create an order
        order = Order.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='Test City'
        )

        # Create an order item
        OrderItem.objects.create(order=order, product=product, price=10.00, quantity=1)

        # Call the function
        send_purchase_notification(order)

        # Assert that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Assert the email subject
        self.assertEqual(mail.outbox[0].subject, f'New Purchase Notification - Order #{order.id}')

        # Assert the recipient
        self.assertIn('admin@gmail.com', mail.outbox[0].to)

        # Assert the email body contains expected content
        self.assertIn('Test Product', mail.outbox[0].body)
        self.assertIn('John Doe', mail.outbox[0].body)
        self.assertIn('john@example.com', mail.outbox[0].body)
        self.assertIn('123-456-7890', mail.outbox[0].body)
        self.assertIn('123 Main St', mail.outbox[0].body)
