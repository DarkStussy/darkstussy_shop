from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import OrderItem, Order


def order_pdf(obj):
    url = reverse('orders:order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_pdf]
    list_filter = ['user', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
