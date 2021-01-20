from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

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
            users.append({'id': u.id,
                          'username': u.username,
                          'role': u.groups.first() if u.groups.count() > 0 else ''})

        return render(request, 'management/user_list.html', {'users': users})
    return render(request, 'bad_permission.html')


def user_edit(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    user = {'id': u.id, 'username': u.username, 'group': u.groups.first() if u.groups.count() > 0 else ''}
    groups = Group.objects.all()
    return render(request, 'management/user_edit.html', {'edit_user': user, 'groups': groups})


def user_save(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.groups.clear()
    gr = request.POST.get('selected_group')
    user.groups.set([gr])
    return redirect('cmsapp:user_list')


def user_delete(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    u.delete()
    return redirect('cmsapp:user_list')

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


def custom_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return render(request, 'account/register.html')


def custom_create_account(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 == pass2:
            user = User.objects.create_user(username=username, email=email, password=pass1)
            user.first_name = fname
            user.last_name = lname
            user.groups.set([3])    # id=3 -> User group
            user.save()

        return render(request, 'account/register.html')
