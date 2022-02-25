from django.shortcuts import render

# Create your views here.
def index(request):
    menu_links = [
        {'href': 'index', 'name': 'домой'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
    ]
    products = [
        {'href': '#', 'img_prod': '/static/img/product-1.jpg', 'alt_txt_prod': '',
         'img_hover': '/static/img/icon-hover.png', 'alt_txt_hover': 'img', 'description': 'Отличный стул',
         'extra_description': 'Расположитесь комфортно. '},

        {'href': '#', 'img_prod': '/static/img/product-2.jpg', 'alt_txt_prod': '',
         'img_hover': '/static/img/icon-hover.png', 'alt_txt_hover': '', 'description': 'Стул повышенного качества',
         'extra_description': 'Не оторваться. '},
    ]
    return render(request, 'mainapp/index.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': menu_links,
        'title': 'магазин',
        'class_name': 'slider',
        'products': products,
    })


def contact(request):
    menu_links = [
        {'href': 'index', 'name': 'домой'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
    ]
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
        'menu_links': menu_links,
        'title': 'контакты',
        'class_name': 'hero',
        'products': products,
    })


def products(request):
    menu_links = [
        {'href': 'index', 'name': 'домой'},
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
    ]
    products = [
        {'href': '#', 'img_prod': '/static/img/product-11.jpg', 'alt_txt_prod': '',
         'img_hover': '/static/img/icon-hover.png', 'alt_txt_hover': 'img', 'description': 'Отличная лампа',
         'extra_description': 'Светло как днем. '},

        {'href': '#', 'img_prod': '/static/img/product-21.jpg', 'alt_txt_prod': '',
         'img_hover': '/static/img/icon-hover.png', 'alt_txt_hover': 'img', 'description': 'Стул повышенного качества',
         'extra_description': 'Не оторваться. '},

        {'href': '#', 'img_prod': '/static/img/product-31.jpg', 'alt_txt_prod': '',
         'img_hover': '/static/img/icon-hover.png', 'alt_txt_hover': 'img', 'description': 'Прекрасный светильник',
         'extra_description': 'Сделает уютной вашу квартиру. '},
    ]
    return render(request, 'mainapp/products.html', context={
        'date': 'сегодняшняя дата: ',
        'menu_links': menu_links,
        'title': 'каталог',
        'class_name': 'hero-white',
        'products': products,
    })