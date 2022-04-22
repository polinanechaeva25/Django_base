from cartapp.models import Cart


def cart(request):
    print(f'context processor cart works')
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related()
    return {
        'cart': cart,
        'cart_items': cart,
        }
