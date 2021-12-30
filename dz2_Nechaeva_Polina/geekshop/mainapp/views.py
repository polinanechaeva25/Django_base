from django.shortcuts import render
from .models import Product, ProductCategory
from django.shortcuts import get_object_or_404

MENU_LINKS = [
    {'href': 'index', 'active_if': ['index'], 'name': 'домой'},
    {'href': 'products:index', 'active_if': ['products:index', 'products:category'], 'name': 'продукты'},
    {'href': 'contact', 'active_if': ['contact'], 'name': 'контакты'},
]


def index(request):
    products = Product.objects.all()[:3]

    return render(request, 'mainapp/index.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'магазин',
        'class_name': 'slider',
        'products': products,
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
    return render(request, 'mainapp/contact.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'контакты',
        'class_name': 'hero',
        'products': products,
    })


def products(request, pk=None):
    if not pk:
        selected_category = ProductCategory.objects.first()
    else:
        selected_category = get_object_or_404(ProductCategory, id=pk)

    products = Product.objects.filter(category=selected_category)
    categories = ProductCategory.objects.all()
    image = [
        {'img': 'img/controll.jpg'},

        {'img': 'img/controll1.jpg'},

        {'img': 'img/controll2.jpg'},
    ]
    return render(request, 'mainapp/products.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': MENU_LINKS,
        'title': 'каталог',
        'class_name': 'hero-white',
        'products': products,
        'categories': categories,
        'image': image,
        'selected_category': selected_category
    })