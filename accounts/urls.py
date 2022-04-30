from django.urls import path

from . import views

app_name = 'c_accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('log-in/', views.login_user, name='login-user'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
    path('profile/', views.profile, name='profile'),
]
