from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View



def logout_views(request):
    user_logout(request)
    return HttpResponseRedirect("/")


class HomeView(View):
    template_name = 'home.html'
    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
        login = request.POST.get("login")
        password = request.POST.get("password")
        user = authenticate(request, username=login, password=password, )
        if user is not None:
            user_login(request, user)
            return HttpResponseRedirect("/home")
        else:
            return render(request, "login.html")


class RegistrationView(View):
    template_name = 'registration.html'
    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
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


class AccountView(View):
    template_name = 'account.html'
    def get(self, request):
        return render(request, self.template_name)