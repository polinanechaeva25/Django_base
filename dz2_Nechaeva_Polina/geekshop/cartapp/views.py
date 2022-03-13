from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from mainapp.models import Product
from cartapp.models import Cart
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def cart(request):
    title = 'корзина'
    cart_items = Cart.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'cart_items': cart_items,
    }

    return render(request, 'cartapp/cart.html', content)


@login_required
def add_to_cart(request, pk=None):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    cart_product = Cart.objects.filter(user=request.user, product=product).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

    cart_product.quantity += 1
    cart_product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_cart(request, pk):
    cart_record = get_object_or_404(Cart, pk=pk)
    cart_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_edit(request, pk, quantity):
    quantity = int(quantity)
    new_cart_item = Cart.objects.get(pk=int(pk))

    if quantity > 0:
        new_cart_item.quantity = quantity
        new_cart_item.save()
    else:
        new_cart_item.delete()

    cart_items = Cart.objects.filter(user=request.user). \
        order_by('product__category')

    content = {
        'cart_items': cart_items,
    }

    result = render_to_string('cartapp/includes/inc_cart_list.html', content)

    return JsonResponse({'result': result})