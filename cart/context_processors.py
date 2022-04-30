from cart.models import Cart


def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        cart = None
    return {'cart': cart}


def get_total_price_of_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        total_price = None
    else:
        total_price = 0
        for item in cart.items.all():
            total_price += item.total_price()
    return {"total_price": total_price}


def get_amount_items(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        amount_items = None
    else:
        amount_items = cart.items.count()
    return {"amount_items": amount_items}
