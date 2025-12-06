from .models import Order, OrderItem
from products.models import Product


def get_cart_items_and_total_for_order(cart_session):
    """
    Calculate cart items and total price for order creation.

    Args:
        cart_session (dict): The cart dictionary from session.

    Returns:
        tuple: (cart_items list, total_price float)
    """
    cart_items = []
    total_price = 0
    for pid, qty in cart_session.items():
        try:
            product = Product.objects.get(id=pid)
            item_total = product.price * qty
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total_price': item_total
            })
        except Product.DoesNotExist:
            continue
    return cart_items, total_price


def create_order_from_cart(user, cart_session, order_data):
    """
    Create an order from the cart session.

    Args:
        user: The user placing the order.
        cart_session (dict): The cart dictionary from session.
        order_data (dict): Order data from the form.

    Returns:
        Order: The created order instance.
    """
    order = Order.objects.create(
        user=user,
        first_name=order_data['first_name'],
        last_name=order_data['last_name'],
        email=order_data['email'],
        address=order_data['address'],
        postal_code=order_data['postal_code'],
        city=order_data['city'],
    )

    # Add items from cart to order
    for pid, qty in cart_session.items():
        try:
            product = Product.objects.get(id=pid)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=qty
            )
        except Product.DoesNotExist:
            continue

    return order
