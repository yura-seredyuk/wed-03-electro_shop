from django.shortcuts import render, get_object_or_404

import shop
from .models import Product, Brand, Category

# Create your views here.

def homepage(request):
    return render(request, 'pages/index.html')

def store(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    brand = None
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.objects.filter(category=category)
    return render(request, 'pages/store.html', {'category':category,
                                                'categories':categories,
                                                'products':products})