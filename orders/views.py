from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product
from notifications.utils import send_purchase_notification

@login_required
def checkout(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # If cart is empty, redirect to cart detail
    if not cart:
        return redirect('cart:cart_detail')
    
    # Calculate total price
    total_price = 0
    cart_items = []
    
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
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
        )
        
        # Add items from cart to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity']
            )
        
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
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})
