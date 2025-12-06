from products.models import Product


def get_cart_items_and_total(cart_session):
    """
    Calculate cart items and total price from session cart.

    Args:
        cart_session (dict): The cart dictionary from session.

    Returns:
        tuple: (cart_items list, total_price float)
    """
    cart_items = []
    total_price = 0
    for pid, qty in cart_session.items():
        try:
            p = Product.objects.get(id=pid)
            item_total = p.price * qty
            total_price += item_total
            cart_items.append({'product': p, 'quantity': qty, 'total_price': item_total})
        except Product.DoesNotExist:
            continue
    return cart_items, total_price


def clean_cart(cart_session):
    """
    Remove invalid products from cart session.

    Args:
        cart_session (dict): The cart dictionary from session.

    Returns:
        dict: Cleaned cart dictionary.
    """
    cleaned_cart = {}
    for pid, qty in cart_session.items():
        if Product.objects.filter(id=pid).exists():
            cleaned_cart[pid] = qty
    return cleaned_cart
