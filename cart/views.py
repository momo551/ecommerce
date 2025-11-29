from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Product

# Cart functionality using sessions

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total
            })
        except Product.DoesNotExist:
            # Remove invalid product from cart
            del cart[product_id]
            request.session['cart'] = cart
    
    return render(request, 'cart/detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@require_POST
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    # Get quantity from request
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    
    # Add to cart
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    request.session['cart'] = cart
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_items_count': sum(cart.values())
        })
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, 'Item removed from cart!')
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    
    # Get quantity from request
    try:
        quantity = int(request.POST.get('quantity', 0))
    except (ValueError, TypeError):
        quantity = 0
    
    if quantity <= 0:
        # Remove item if quantity is 0 or less
        if str(product_id) in cart:
            del cart[str(product_id)]
    else:
        # Update quantity
        cart[str(product_id)] = quantity
    
    request.session['cart'] = cart
    
    # Calculate total price
    total_price = 0
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            total_price += product.price * qty
        except Product.DoesNotExist:
            pass
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_price': f'{total_price:.2f}'
        })
    
    return redirect('cart:cart_detail')
