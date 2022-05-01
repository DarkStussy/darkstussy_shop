from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput
from django import forms

from orders.models import Order


class OrderForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    email = forms.EmailField(widget=HiddenInput())

    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
