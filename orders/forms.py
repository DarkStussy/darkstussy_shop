from django.forms import ModelForm, HiddenInput
from django import forms

from orders.models import Order


class OrderForm(ModelForm):
    email = forms.EmailField(widget=HiddenInput())

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
