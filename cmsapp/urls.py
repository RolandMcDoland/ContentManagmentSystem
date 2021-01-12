from django.urls import path

from . import views

app_name = 'cmsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('manage/articles', views.article_list, name='article_list'),
    path('manage/comments', views.comment_list, name='comment_list'),
    path('manage/users', views.user_list, name='user_list'),
    path('account/login', views.custom_login, name='login'),
    path('account/logout', views.custom_logout, name='logout'),
    path('account/authentication', views.custom_authentication, name='authentication'),
]
