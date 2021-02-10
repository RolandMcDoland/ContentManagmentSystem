import datetime
import pathlib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.conf import settings
from .models import Article, Comment, User, Tag, Section


def index(request):
    articles = Article.objects.filter(published_date__lte=datetime.datetime.now()).order_by('edited_date')
    for a in articles:
        with open(a.path, 'r') as f:
            a.short_content = f.read()[:100]

    sections = Section.objects.all()
    return render(request, 'index.html', {'articles': articles, 'sections': sections})


def article_section(request, section_id):
    articles = Article.objects.filter(published_date__lte=datetime.datetime.now(), section_id__id=section_id).order_by('edited_date')
    for a in articles:
        with open(a.path, 'r') as f:
            a.short_content = f.read()[:100]

    sections = Section.objects.all()
    section = Section.objects.filter(id=section_id).first()
    return render(request, 'index.html', {'articles': articles, 'sections': sections, 'section': section})


def article_read(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    with open(article.path, 'r') as f:
        article.content = f.read()
    comments = Comment.objects.filter(article_id_id__exact=article_id).order_by('published_date').reverse()
    t = Tag.objects.filter(article_id__id=article.id)
    tag_string = ''
    for tag in t:
        tag_string += tag.name
        tag_string += '   '

    return render(request, 'article.html', {'article': article, 'comments': comments, 'tags': tag_string})


def article_list(request):
    if request.user.is_superuser:
        articles = Article.objects.order_by('created_date')

        data = []

        for article in articles:
            t = Tag.objects.filter(article_id__id=article.id)
            tag_string = ''
            for tag in t:
                tag_string += tag.name
                tag_string += ';'
            
            d = { "article" : article, "tags" : tag_string }
            data.append(d)          

        return render(request, 'management/article_list.html', {'articles': data})
    return render(request, 'bad_permission.html')


def comment_list(request):
    if request.user.is_superuser:
        comments = Comment.objects.order_by('article_id')
        return render(request, 'management/comment_list.html', {'comments': comments})
    return render(request, 'bad_permission.html')


def comment_new(request, article_id):
    comment = Comment(article_id=get_object_or_404(Article, pk=article_id), user_id=request.user, text=request.POST.get('commentText'))
    comment.save()
    return redirect('cmsapp:article_read', article_id)


def section_list(request):
    if request.user.is_superuser:
        sections = Section.objects.order_by('name')
        return render(request, 'management/section_list.html', {'sections': sections})
    return render(request, 'bad_permission.html')


def section_new(request):
    return render(request, 'management/section_new.html')


def section_save(request):
    section = Section(name=request.POST.get('name'))
    section.save()
    return redirect('cmsapp:section_list')


def section_delete(request, section_id):
    s = get_object_or_404(Section, pk=section_id)
    s.delete()
    return redirect('cmsapp:section_list')


def section_edit(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    return render(request, 'management/section_edit.html', {'section': section})


def section_edit_save(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    section.name = request.POST.get('name')
    section.save()
    return redirect('cmsapp:section_list')


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
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    sections = Section.objects.all()
    return render(request, 'management/article_new.html', {'date': date, 'sections': sections})


def article_save(request):
    path = settings.MEDIA_ROOT + 'articles/' + request.POST.get("title") + '_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'

    pathlib.Path(settings.MEDIA_ROOT + 'articles').mkdir(parents=True, exist_ok=True)
    with open(path, 'a+') as f:
        f.write(request.POST.get("content").replace('\n', ''))

    section = Section.objects.filter(name=request.POST.get('section')).first()

    article = Article(name=request.POST.get("title"), user_id=request.user, published_date=request.POST.get("publishDate"), path=path, section_id=section)
    article.save()

    for tag_name in request.POST.get("tags").split(';'):
        if tag_name != '':
            t = Tag.objects.filter(name=tag_name)
            if not t:
                tag = Tag(name=tag_name)
                tag.save()
                tag.article_id.add(article)
            else:
                t[0].article_id.add(article)

    return redirect('cmsapp:article_list')


def article_edit(request, article_id):
    if request.user.is_superuser:
        article = Article.objects.filter(pk=article_id).first()

        with open(article.path, 'r') as f:
            article.content = f.read()

        t = Tag.objects.filter(article_id__id=article.id)
        tag_string = ''
        for tag in t:
            tag_string += tag.name
            tag_string += ';'

        sections = Section.objects.all()

        return render(request, 'management/article_edit.html', {'article': article, 'tags': tag_string, 'sections': sections})
    return render(request, 'bad_permission.html')


def article_edit_save(request, article_id):
    article = Article.objects.filter(pk=article_id).first()
    article.name = request.POST.get("title")
    article.published_date = request.POST.get("publishDate")

    section = Section.objects.filter(name=request.POST.get('section')).first()
    article.section_id = section

    # article.path = request.POST.get("path")
    # article.content = request.POST.get("content")

    path = article.path
    with open(path, 'w') as f:
        f.write(request.POST.get("content").replace('\n', ''))

    article.save()

    for tag_name in request.POST.get("tags").split(';'):
        if tag_name != '':
            t = Tag.objects.filter(name=tag_name, article_id__id=article.id)
            if not t:
                t = Tag.objects.filter(name=tag_name)
                if not t:
                    tag = Tag(name=tag_name)
                    tag.save()
                    tag.article_id.add(article)
                else:
                    t[0].article_id.add(article)
        
    t = Tag.objects.filter(article_id__id=article.id)
    for tag in t:
        if tag.name not in request.POST.get("tags").split(';'):
            a = tag.article_id.all()
            if len(a) == 1:
                tag.delete()
            else:
                tag.article_id.remove(article)

    return redirect('cmsapp:article_list')


def article_delete(request, article_id):
    a = get_object_or_404(Article, pk=article_id)
    a.delete()
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
