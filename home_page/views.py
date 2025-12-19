from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.

def login_views(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        user = authenticate(request, username=login, password=password, )
        if user is not None:
            user_login(request, user)
            return HttpResponseRedirect("/home")
        else:
            return render(request, "login.html")
    return render(request, 'login.html')

def registration_views(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            User.objects.create_user(username=login, password=password)
            user = authenticate(request, username=login, password=password)
            if user is not None:
                user_login(request, user)
                return HttpResponseRedirect("/home")
            else:
                return render(request, "login.html")
    return render(request, 'registration.html')

def logout_views(request):
    user_logout(request)
    return HttpResponseRedirect("/")

def home_views(request):
    return render(request, 'home.html')