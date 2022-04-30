from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cart.models import Cart
from orders.forms import OrderForm
from orders.models import OrderItem


@login_required
def create(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.count() == 0:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart.items.all():
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)
                    item.delete()
                return render(request, 'orders/created.html', {'order': order})
            else:
                messages.error(request, "Form isn't valid!")
                return redirect('orders:create')

        form = OrderForm(initial={'email': request.user.email})
        return render(request, 'orders/create.html', {'order_form': form})
    else:
        messages.error(request, 'Cart is empty')
        return redirect('cart:cart_detail')
