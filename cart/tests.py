from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Category, Product

class CartViewsTest(TestCase):
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
    
    def test_cart_detail_page(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), {
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart.get(str(self.product.id)), 2)
    
    def test_remove_from_cart(self):
        # First add item to cart
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {
            'quantity': 2
        })
        
        # Then remove it
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after removing from cart
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)
    
    def test_update_cart(self):
        # First add item to cart
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {
            'quantity': 2
        })
        
        # Then update quantity
        response = self.client.post(reverse('cart:cart_update', args=[self.product.id]), {
            'quantity': 5
        })
        self.assertEqual(response.status_code, 302)  # Redirect after updating cart
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart.get(str(self.product.id)), 5)
