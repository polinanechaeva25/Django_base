from django.shortcuts import render
from .models import Product, ProductCategory
from cartapp.models import Cart
from django.shortcuts import get_object_or_404
from django.urls import reverse
import random

MENU_LINKS = [
    {'href': 'index', 'active_if': ['index'], 'name': 'домой'},
    {'href': 'products:index', 'active_if': ['products:index', 'products:category'], 'name': 'продукты'},
    {'href': 'contact', 'active_if': ['contact'], 'name': 'контакты'},
]


def index(request):
    products = Product.objects.all()[:3]
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    return render(request, 'mainapp/index.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'магазин',
        'class_name': 'slider',
        'products': products,
        'cart': cart,
    })


def contact(request):
    products = [
        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},

        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},

        {'city': 'Москва', 'phone_number': '+7-888-888-8888', 'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД'},
    ]
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    return render(request, 'mainapp/contact.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'контакты',
        'class_name': 'hero',
        'products': products,
        'cart': cart,
    })


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all().filter(is_active=True),
        'product': get_object_or_404(Product, pk=pk),
        'cart': get_cart(request.user),
        'menu_links': MENU_LINKS,
        'class_name': 'hero-white',
    }

    return render(request, 'mainapp/product.html', content)


def get_cart(user):
    if user.is_authenticated:
        return Cart.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


def products(request, pk=None):
    # import pdb; pdb.set_trace()
    cart = get_cart(request.user)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    if not pk:
        if pk == 0:
            selected_category = 0
            selected_category_dict = {"name": 'Всё', "href": reverse('products:category', args=[0])}
        else:
            selected_category = None
            selected_category_dict = None
    else:
        selected_category = get_object_or_404(ProductCategory, id=pk)
        selected_category_dict = {"name": selected_category.name,
                                  "href": reverse('products:category', args=[selected_category.id])}
    if selected_category:
        products = Product.objects.filter(category=selected_category)[:3]
    else:
        products = Product.objects.all()[:3]
    image = [
        {'img': 'img/controll.jpg'},

        {'img': 'img/controll1.jpg'},
        {'img': 'img/controll2.jpg'},
    ]
    categories = ProductCategory.objects.all().filter(is_active=True)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'каталог',
        'class_name': 'hero-white',
        'products': products,
        'image': image,
        'selected_category': selected_category_dict,
        'cart': cart,
        'categories': categories,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    if pk is None:

        return render(request, 'mainapp/products_index.html', context)

    return render(request, 'mainapp/products.html', context)
