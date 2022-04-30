from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.cart.user.username + ' - ' + self.product.name
