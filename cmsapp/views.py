from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Article, Comment, User


def index(request):
    # return HttpResponse("Hello world! It's working!")
    return render(request, 'index.html')


def article_list(request):
    if request.user.is_superuser:
        articles = Article.objects.order_by('created_date')
        return render(request, 'management/article_list.html', {'articles': articles})
    return render(request, 'bad_permission.html')


def comment_list(request):
    if request.user.is_superuser:
        comments = Comment.objects.order_by('article_id')
        return render(request, 'management/comment_list.html', {'comments': comments})
    return render(request, 'bad_permission.html')


def user_list(request):
    if request.user.is_superuser:
        temp_users = User.objects.order_by('id')
        users = []
        for u in temp_users:
            users.append({'username': u.username, 'role': 'admin'})

        return render(request, 'management/user_list.html', {'users': users})
    return render(request, 'bad_permission.html')

def article_new(request):
    return render(request, 'management/article_new.html')

def article_save(request):
    article = Article(name = request.POST.get("title"), user_id = request.user, published_date = request.POST.get("publishDate"), path = request.POST.get("path"))
    article.save()
    return redirect('cmsapp:article_list')


def custom_login(request):
    return render(request, 'account/login.html')


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def custom_authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect('/')
    else:
        return render(request, 'account/login.html', {'error': True})
