from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from products.models import Category, Product
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test Street',
            postal_code='12345',
            city='Test City'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test product description',
            price=19.99
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=19.99,
            quantity=2
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.first_name, 'Test')
        self.assertEqual(self.order.last_name, 'User')
        self.assertEqual(self.order.email, 'test@example.com')
        self.assertEqual(str(self.order), f'Order {self.order.id}')
    
    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, 19.99)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(str(self.order_item), str(self.order_item.id))
    
    def test_order_total_cost(self):
        expected_total = Decimal('19.99') * 2  # price * quantity
        self.assertEqual(self.order.get_total_cost(), expected_total)

class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test product description',
            price=19.99
        )
    
    def test_checkout_requires_login(self):
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_checkout_page_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        # Add item to cart first
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)
    
    def test_order_history_requires_login(self):
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_history_page_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 200)
