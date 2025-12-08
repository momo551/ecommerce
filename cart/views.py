from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def cart_detail(request):
    """
    Display the cart details including items and total price.
    """
    from .services import get_cart_items_and_total
    cart = request.session.get('cart', {})
    cart_items, total_price = get_cart_items_and_total(cart)
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})

@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or increase its quantity.
    """
    from products.models import Product
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        cart_items_count = sum(cart.values())
        from .services import get_cart_items_and_total
        _, total_price = get_cart_items_and_total(cart)
        return JsonResponse({
            'success': True,
            'cart_items_count': cart_items_count,
            'total_price': f'${total_price:.2f}'
        })
    else:
        # Regular POST request
        return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('quantity', 0))
    if qty <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = qty
    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        from .services import get_cart_items_and_total
        _, total_price = get_cart_items_and_total(cart)
        return JsonResponse({
            'success': True,
            'total_price': f'${total_price:.2f}'
        })
    else:
        # Regular POST request
        return redirect('cart:cart_detail')
