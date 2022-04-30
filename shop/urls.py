from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:page>/', views.product_list, name='product_list'),
    path('products/<int:page>/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('detail/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
