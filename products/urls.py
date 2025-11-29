from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<slug:category_slug>/', views.product_list, name='category_detail'),
    path('products/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]
