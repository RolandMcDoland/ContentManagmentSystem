from django.urls import path

from . import views

app_name = 'cmsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<int:article_id>', views.article_read, name='article_read'),
    path('comments/new/<int:article_id>', views.comment_new, name='comment_new'),
    path('manage/articles', views.article_list, name='article_list'),
    path('manage/comments', views.comment_list, name='comment_list'),
    path('manage/users', views.user_list, name='user_list'),
    path('manage/users/edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('manage/users/edit/save/<int:user_id>', views.user_save, name='user_save'),
    path('manage/users/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('manage/articles/new', views.article_new, name='article_new'),
    path('manage/articles/new/save', views.article_save, name='article_save'),
    path('manage/articles/delete/<int:article_id>', views.article_delete, name='article_delete'),
    path('manage/articles/edit/<str:name>', views.article_edit, name='article_edit'),
    path('manage/articles/edit', views.article_edit_save, name='article_edit_save'),
    path('account/login', views.custom_login, name='login'),
    path('account/register', views.custom_register, name='register'),
    path('account/logout', views.custom_logout, name='logout'),
    path('account/authentication', views.custom_authentication, name='authentication'),
    path('account/createaccount', views.custom_create_account, name='create_account'),
]
