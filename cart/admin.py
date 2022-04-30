from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']


@admin.register(Cart)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created']
    list_filter = ['user', 'created']
    inlines = [CartItemInline]
