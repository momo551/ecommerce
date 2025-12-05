from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

def cart_detail(request):
    from products.models import Product
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
            item_total = p.price * qty
            total_price += item_total
            cart_items.append({'product': p, 'quantity': qty, 'total_price': item_total})
        except Product.DoesNotExist:
            continue
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})

@require_POST
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
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
    return redirect('cart:cart_detail')
