from django.urls import path

from . import views

app_name = 'cmsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('manage/articles', views.article_list, name='article_list'),
    path('manage/comments', views.comment_list, name='comment_list'),
    path('manage/users', views.user_list, name='user_list'),
    path('manage/users/edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('manage/users/edit/save/<int:user_id>', views.user_save, name='user_save'),
    path('manage/users/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('manage/articles/new', views.article_new, name='article_new'),
    path('manage/articles/new/save', views.article_save, name='article_save'),
    path('account/login', views.custom_login, name='login'),
    path('account/register', views.custom_register, name='register'),
    path('account/logout', views.custom_logout, name='logout'),
    path('account/authentication', views.custom_authentication, name='authentication'),
    path('account/createaccount', views.custom_create_account, name='create_account'),
]
