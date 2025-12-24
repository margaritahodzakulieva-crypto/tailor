from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import PostForm, UserProfileForm
from .models import Post


def logout_views(request):
    user_logout(request)
    return HttpResponseRedirect("/")


class HomeView(View):
    template_name = 'home.html'
    def get(self, request):
        posts = Post.objects.all()
        return render(request, self.template_name, context={
            'user_posts': posts
        })


class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_login(request, user)
            messages.success(request, 'Welcome!')
            return redirect('/home')
        else:
            messages.error(request, 'Invalid login or password')
            return render(request, self.template_name, {'form': form})


class RegistrationView(View):
    template_name = 'registration.html'
    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('/home')
        else:
            messages.error(request, 'Registration failed!')
            return render(request, self.template_name, {'form': form})


class AccountView(View):
    template_name = 'account.html'
    def get(self, request):
        profile = request.user.profile
        posts = Post.objects.filter(user=request.user).order_by('-date_posted')
        return render(request, self.template_name, context={
            'profile': profile,
            'user_posts': posts
        })

class RedactionAccountView(View):
    template_name = 'redaction_account.html'
    def get(self, request):
        form = UserProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        return render(request, self.template_name, {'form': form})