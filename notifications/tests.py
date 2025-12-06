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
        self.assertIn('momo55265526@gmail.com', mail.outbox[0].to)

        # Assert the email body contains expected content
        self.assertIn('Test Product', mail.outbox[0].body)
        self.assertIn('John Doe', mail.outbox[0].body)
        self.assertIn('john@example.com', mail.outbox[0].body)
        self.assertIn('123 Main St', mail.outbox[0].body)

    def test_send_purchase_notification_multiple_items(self):
        # Create a user
        user = User.objects.create_user(username='testuser2', email='test2@example.com', password='password')

        # Create a category
        category = Category.objects.create(name='Test Category', slug='test-category')

        # Create products
        product1 = Product.objects.create(name='Test Product 1', slug='test-product-1', description='Test Description 1', price=10.00, category=category)
        product2 = Product.objects.create(name='Test Product 2', slug='test-product-2', description='Test Description 2', price=20.00, category=category)

        # Create an order
        order = Order.objects.create(
            user=user,
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            address='456 Elm St',
            postal_code='67890',
            city='Another City'
        )

        # Create multiple order items
        OrderItem.objects.create(order=order, product=product1, price=10.00, quantity=2)
        OrderItem.objects.create(order=order, product=product2, price=20.00, quantity=1)

        # Call the function
        send_purchase_notification(order)

        # Assert that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Assert the email subject
        self.assertEqual(mail.outbox[0].subject, f'New Purchase Notification - Order #{order.id}')

        # Assert the recipient
        self.assertIn('momo55265526@gmail.com', mail.outbox[0].to)

        # Assert the email body contains expected content for multiple items
        self.assertIn('Test Product 1', mail.outbox[0].body)
        self.assertIn('Test Product 2', mail.outbox[0].body)
        self.assertIn('Jane Smith', mail.outbox[0].body)
        self.assertIn('jane@example.com', mail.outbox[0].body)
        self.assertIn('456 Elm St', mail.outbox[0].body)
        self.assertIn('Quantity: 2', mail.outbox[0].body)
        self.assertIn('Quantity: 1', mail.outbox[0].body)

    def test_send_purchase_notification_email_content_detailed(self):
        # Create a user
        user = User.objects.create_user(username='testuser3', email='test3@example.com', password='password')

        # Create a category
        category = Category.objects.create(name='Test Category', slug='test-category')

        # Create a product
        product = Product.objects.create(name='Detailed Product', slug='detailed-product', description='Detailed Description', price=15.50, category=category)

        # Create an order
        order = Order.objects.create(
            user=user,
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            address='789 Oak St',
            postal_code='54321',
            city='Detail City'
        )

        # Create an order item
        OrderItem.objects.create(order=order, product=product, price=15.50, quantity=3)

        # Call the function
        send_purchase_notification(order)

        # Assert that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Get the email body
        email_body = mail.outbox[0].body

        # Assert detailed content
        self.assertIn('New Purchase Notification - Order #', mail.outbox[0].subject)
        self.assertIn('Bob Johnson', email_body)
        self.assertIn('bob@example.com', email_body)
        self.assertIn('789 Oak St', email_body)
        self.assertIn('Detail City', email_body)
        self.assertIn('54321', email_body)
        self.assertIn('Detailed Product', email_body)
        self.assertIn('Quantity: 3', email_body)
        self.assertIn('Price: $15.50', email_body)
        self.assertIn('Total Cost: $46.50', email_body)  # Assuming get_total_cost works
        self.assertIn('Order Date:', email_body)
