from django.shortcuts import render, get_object_or_404
from django.urls.conf import path
from shop.models import Product, Brand, Category
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.conf import settings


def home_page(request):
    return render(request, 'pages/index.html', {'count':count(request)})


def store_page(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    brand = None
    Brands = Brand.objects.all()

    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.objects.filter(category=category)
    cart_product_form = CartAddProductForm()
    cart_items =  request.session.get(settings.CART_SESSION_ID)
    pr = []
    if cart_items:
        product = cart_items.keys()   
        pr = Product.objects.filter(id__in=product)
        print(pr)        
    return render(request, 'pages/store.html', {'category': category,
                                                'categories': categories,
                                                'products': products,
                                                'cart_product_form': cart_product_form,
                                                'count':count(request),
                                                'cart_items':pr,
                                                'cart':cart(request)})


def product_page(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    cart_product_form = CartAddProductForm()
    return render(request, 'pages/product.html', {'product_detail': product,
                                                  'cart_product_form': cart_product_form,
                                                  'count':count(request)})


def checkout_page(request):
    return render(request, 'pages/checkout.html')

def count(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    print(cart)
    count = 0
    if cart:
        cart_values = cart.values()
        
        subtotal = 0
        for item in cart_values:
            count += item['quantity']
            subtotal += item['quantity'] * float(item['price'])

        cart_items_id = cart.keys()   
        product_list = Product.objects.filter(id__in=cart_items_id)
    
    return count

def cart(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    print(cart)
    count = 0
    subtotal = 0
    product_list = []
    if cart:
        cart_values = cart.values()
        for item in cart_values:
            count += item['quantity']
            subtotal += item['quantity'] * float(item['price'])
        cart_items_id = cart.keys()   
        product_list = Product.objects.filter(id__in=cart_items_id)
    return {'count':count, 'product_list':product_list, 'cart':cart, 'subtotal':subtotal}


