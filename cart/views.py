from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.models import Cart, CartItem
from cart.forms import CartAddProductForm
from shop.models import Product


@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = 0
    for item in cart_items:
        total_price += item.total_price()
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
def cart_add(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        try:
            cart_item = cart.items.get(product=product)
        except CartItem.DoesNotExist:
            CartItem.objects.create(product=product, quantity=quantity, price=product.price, cart=cart)
        else:
            cart_item.quantity = int(cd['quantity'])
            cart_item.save()

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart.items.get(product=product).delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart_detail')
