from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    # return HttpResponse("Hello world! It's working!")
    return render(request, 'index.html')


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
