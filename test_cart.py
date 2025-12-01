import os
import django
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

def test_cart_functionality():
    client = Client()

    # Get the product
    product = Product.objects.first()
    if not product:
        print("No products in database")
        return

    print(f"Testing with product: {product.name}, price: ${product.price}")

    # Test 1: Add product with quantity 1
    response = client.post(reverse('cart:cart_add', args=[product.id]), {'quantity': 1})
    print(f"Add qty 1: Status {response.status_code}")

    # Check cart
    response = client.get(reverse('cart:cart_detail'))
    print(f"Cart detail: Status {response.status_code}")

    # Parse cart from session
    cart = client.session.get('cart', {})
    print(f"Cart after add 1: {cart}")

    # Test 2: Add same product with quantity 2 (should accumulate to 3)
    response = client.post(reverse('cart:cart_add', args=[product.id]), {'quantity': 2})
    print(f"Add qty 2: Status {response.status_code}")

    cart = client.session.get('cart', {})
    print(f"Cart after add 2: {cart}")

    # Test 3: Add same product with quantity 1 (should accumulate to 4)
    response = client.post(reverse('cart:cart_add', args=[product.id]), {'quantity': 1})
    print(f"Add qty 1: Status {response.status_code}")

    cart = client.session.get('cart', {})
    print(f"Cart after add 1 more: {cart}")

    # Test 4: Update quantity to 5
    response = client.post(reverse('cart:cart_update', args=[product.id]), {'quantity': 5})
    print(f"Update to qty 5: Status {response.status_code}")

    cart = client.session.get('cart', {})
    print(f"Cart after update to 5: {cart}")

    # Test 5: Remove product
    response = client.post(reverse('cart:cart_remove', args=[product.id]))
    print(f"Remove product: Status {response.status_code}")

    cart = client.session.get('cart', {})
    print(f"Cart after remove: {cart}")

    print("Test completed")

if __name__ == '__main__':
    test_cart_functionality()
