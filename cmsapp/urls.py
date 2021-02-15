from django.urls import path

from . import views

app_name = 'cmsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('articles/section/<int:section_id>', views.article_section, name='article_section'),
    path('articles/<int:article_id>', views.article_read, name='article_read'),
    path('comments/new/<int:article_id>', views.comment_new, name='comment_new'),
    path('manage/articles', views.article_list, name='article_list'),
    path('manage/comments', views.comment_list, name='comment_list'),
    path('manage/comments/edit/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('manage/comments/edit/save/<int:comment_id>', views.comment_edit_save, name='comment_edit_save'),
    path('manage/comments/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('manage/sections', views.section_list, name='section_list'),
    path('manage/sections/new', views.section_new, name='section_new'),
    path('manage/sections/new/save', views.section_save, name='section_save'),
    path('manage/sections/delete/<int:section_id>', views.section_delete, name='section_delete'),
    path('manage/sections/edit/<int:section_id>', views.section_edit, name='section_edit'),
    path('manage/sections/edit/save/<int:section_id>', views.section_edit_save, name='section_edit_save'),
    path('manage/users', views.user_list, name='user_list'),
    path('manage/users/edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('manage/users/edit/save/<int:user_id>', views.user_save, name='user_save'),
    path('manage/users/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('manage/articles/new', views.article_new, name='article_new'),
    path('manage/articles/new/save', views.article_save, name='article_save'),
    path('manage/articles/delete/<int:article_id>', views.article_delete, name='article_delete'),
    path('manage/articles/edit/<int:article_id>', views.article_edit, name='article_edit'),
    path('manage/articles/edit/save/<int:article_id>', views.article_edit_save, name='article_edit_save'),
    path('account/login', views.custom_login, name='login'),
    path('account/register', views.custom_register, name='register'),
    path('account/logout', views.custom_logout, name='logout'),
    path('account/authentication', views.custom_authentication, name='authentication'),
    path('account/createaccount', views.custom_create_account, name='create_account'),
    path('account/profile/edit', views.profile_edit, name='profile_edit'),
    path('account/profile/edit/save/<int:user_id>', views.profile_edit_save, name='profile_edit_save'),
    path('account/profile/password/change/<int:user_id>', views.profile_password_change, name='profile_password_change'),
    path('system/send-email/<int:user_id>', views.send_email, name='send_email')
]
