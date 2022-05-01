from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('orders/', views.view_orders, name='orders'),
    path('<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
]
