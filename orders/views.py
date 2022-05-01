from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from cart.models import Cart
from orders.forms import OrderForm
from orders.models import OrderItem, Order

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


@login_required
def create(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.count() == 0:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart.items.all():
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity,
                                             price=item.price)
                    item.delete()

                return HttpResponseRedirect(reverse('payment:process', args=(order.id,)))
            else:
                messages.error(request, "Form isn't valid!")
                return redirect('orders:create')

        form = OrderForm(initial={'user': request.user, 'email': request.user.email})
        return render(request, 'orders/create.html', {'order_form': form})
    else:
        messages.error(request, 'Cart is empty')
        return redirect('cart:cart_detail')


@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/user_orders.html', {'orders': orders})


def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf = html_to_pdf("orders/pdf.html", {"order": order})
    return HttpResponse(pdf, content_type='application/pdf')
