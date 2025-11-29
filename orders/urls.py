from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('history/', views.order_history, name='order_history'),
]
