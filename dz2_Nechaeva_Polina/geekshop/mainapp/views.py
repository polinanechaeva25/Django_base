from django.shortcuts import render
from .models import Product, ProductCategory
from cartapp.models import Cart
from django.shortcuts import get_object_or_404
from django.urls import reverse
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.http import JsonResponse


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


MENU_LINKS = [
    {'href': 'index', 'active_if': ['index'], 'name': 'домой'},
    {'href': 'products:index', 'active_if': ['products:index', 'products:category'], 'name': 'продукты'},
    {'href': 'contact', 'active_if': ['contact'], 'name': 'контакты'},
]


def index(request):
    title = 'магазин'
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    products = get_products()[:3]
    categories = ProductCategory.objects.all()
    category_id = random.sample(list(categories), 1)[0].id
    content = {
        'title': title,
        'menu_links': MENU_LINKS,
        'class_name': 'slider',
        'products': products,
        'category_id': category_id,
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    products = [
        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},

        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},

        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},
    ]

    return render(request, 'mainapp/contact.html', context={
        'menu_links': MENU_LINKS,
        'title': 'контакты',
        'class_name': 'hero',
        'products': products,

    })


def product(request, pk):
    title = 'продукты'
    # product = get_object_or_404(Product, pk=pk)
    product = get_product(pk)
    links_menu = get_links_menu()
    content = {
        'title': title,
        # 'links_menu': ProductCategory.objects.all().filter(is_active=True),
        'links_menu': links_menu,
        'product': product,
        # 'cart': get_cart(request.user),
        'menu_links': MENU_LINKS,
        'class_name': 'hero-white',
        'selected_category': product.category,
    }

    return render(request, 'mainapp/product.html', content)


def get_hot_product():
    # products = Product.objects.all()
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


@cache_page(3600)
def products(request, pk=None, page=1):
    if not pk:
        if pk == 0:
            selected_category_id = 0
            selected_category = 0
            selected_category_dict = {"name": 'Всё', "href": reverse('products:category', args=[0])}
        else:
            selected_category = None
            selected_category_id = 0
            selected_category_dict = None
    else:
        selected_category = get_object_or_404(ProductCategory, id=pk)
        selected_category_id = selected_category.id
        selected_category_dict = {"name": selected_category.name,
                                  "href": reverse('products:category', args=[selected_category.id])}
    if selected_category:
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()

    image = [
        {'img': 'img/controll.jpg'},

        {'img': 'img/controll1.jpg'},
        {'img': 'img/controll2.jpg'},
    ]
    categories = ProductCategory.objects.all().filter(is_active=True)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'menu_links': MENU_LINKS,
        'title': 'каталог',
        'class_name': 'hero-white',
        'products': products,
        'products_same': Product.objects.all()[:3],
        'products_paginator': products_paginator,
        'image': image,
        'selected_category': selected_category_dict,
        'categories': categories,
        'hot_product': hot_product,
        'same_products': same_products,
        'category_id': selected_category_id,
    }
    if pk is None:
        return render(request, 'mainapp/products_index.html', context)

    return render(request, 'mainapp/products.html', context)



