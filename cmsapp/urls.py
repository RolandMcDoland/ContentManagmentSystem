from django.urls import path

from . import views

app_name = 'cmsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('account/login', views.custom_login, name='login'),
    path('account/logout', views.custom_logout, name='logout'),
    path('account/authentication', views.custom_authentication, name='authentication'),
]

