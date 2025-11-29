from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.description, 'Test description')
        self.assertEqual(str(self.category), 'Test Category')

class ProductModelTest(TestCase):
    def setUp(self):
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
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'Test product description')
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_product_category_relationship(self):
        self.assertEqual(self.product.category, self.category)

class ProductViewsTest(TestCase):
    def setUp(self):
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
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_home_page(self):
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_list_page(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_page(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_search_functionality(self):
        response = self.client.get(reverse('products:search_results'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
