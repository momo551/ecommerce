from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Pagination
    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'products/product_detail.html', {'product': product})

def home(request):
    # Get latest products for homepage
    products = Product.objects.filter(available=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories
    })

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(name__icontains=query)
    
    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/search_results.html', {
        'page_obj': page_obj,
        'query': query
    })
