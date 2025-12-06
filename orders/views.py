from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from notifications.utils import send_purchase_notification

@login_required
def checkout(request):
    """
    Handle the checkout process: display cart items and create order on POST.
    """
    from .services import get_cart_items_and_total_for_order, create_order_from_cart
    from cart.services import clean_cart

    # Get cart from session
    cart = request.session.get('cart', {})

    # If cart is empty, redirect to cart detail
    if not cart:
        return redirect('cart:cart_detail')

    # Clean cart and get items/total
    cart = clean_cart(cart)
    cart_items, total_price = get_cart_items_and_total_for_order(cart)

    if request.method == 'POST':
        # Create order from cart
        order_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'postal_code': request.POST.get('postal_code'),
            'city': request.POST.get('city'),
        }
        order = create_order_from_cart(request.user, cart, order_data)

        # Clear the cart
        request.session['cart'] = {}

        # Send notification to admin
        send_purchase_notification(order)

        # Redirect to payment processing
        return redirect('orders:payment_process', order_id=order.id)

    # Pre-fill form with user's profile data
    profile = request.user.profile if hasattr(request.user, 'profile') else None

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': profile
    }

    return render(request, 'orders/checkout.html', context)

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # For now, we'll just mark the order as paid
    # In a real application, you would integrate with Stripe here
    order.paid = True
    order.save()
    
    return redirect('orders:payment_success', order_id=order.id)

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})

def payment_cancelled(request):
    # Show cancelled page if payment was cancelled
    return render(request, 'orders/cancelled.html')

@login_required
def order_history(request):
    """
    Display the user's order history.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/history.html', {'orders': orders})
