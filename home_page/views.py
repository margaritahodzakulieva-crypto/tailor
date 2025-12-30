from django.contrib.auth import login as user_login, logout as user_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import PostForm, UserProfileForm
from .models import Post, Profile
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def logout_views(request):
    user_logout(request)
    return HttpResponseRedirect("/")


class HomeView(View):
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
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
            login_time = timezone.now()
            subject = 'Successful login'
            message = f"""
                Hi, {user.username}! 👋
                We’re happy to see you again — you’ve successfully signed in to your account 😊
                📅 Date and time of login: {login_time.strftime('%d.%m.%Y %H:%M:%S')}
                If this wasn’t you, please change your password as soon as possible and contact us — we’ll be glad to help.
                With care,
                The Site Team 💙
            """
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Welcome! Notification sent by email')
            except Exception as e:
                messages.warning(request,
                                 'Login was successful, but the email notification was not sent ')
                print(f"Error sending email: {e}")
            messages.success(request, 'Welcome!')
            return redirect('/home')
        else:
            messages.error(request, 'Неверный логин или пароль')
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
    def get(self, request, username=None):
        if username:
            profile_user = get_object_or_404(User, username=username)
        else:
            if not request.user.is_authenticated:
                return redirect('login')
            profile_user = request.user
        user_posts = Post.objects.filter(user=profile_user).order_by('-date_posted')
        return render(request, self.template_name, {
            'profile_user': profile_user,
            'user_posts': user_posts,
        })


class RedactionAccountView(View):
    template_name = 'redaction_account.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        form = UserProfileForm(instance=profile)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        return render(request, self.template_name, {'form': form})


class PostView(View):
    template_name = 'post.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, self.template_name, context={
            'post': post,
            'profile': request.user.profile if request.user.is_authenticated else None,
        })


class AddPostView(View):
    template_name = 'add_post.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, context={
            'form': form,
            'profile': request.user.profile if request.user.is_authenticated else None,
        })
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/home')
        return render(request, self.template_name, context={
            'form': form,
            'profile': request.user.profile if request.user.is_authenticated else None,
        })


def search_results(request):
    query = request.GET.get('q', '').strip()
    posts = []
    if query:
        posts = Post.objects.filter(
            Q(post_title__icontains=query) |
            Q(post_description__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()
    context = {
       'query': query,
        'posts': posts,
    }
    return render(request, 'search_results.html', context)