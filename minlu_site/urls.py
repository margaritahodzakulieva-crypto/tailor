from django.contrib import admin
from django.urls import path
from home_page.views import logout_views, HomeView, LoginView, RegistrationView, AccountView, RedactionAccountView, PostView, AddPostView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('logout/', logout_views),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('home/',HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),
    path('user/<str:username>/', AccountView.as_view(), name='user_profile'),
    path('redaction/', RedactionAccountView.as_view(), name='edit_account'),
    path('post/<int:pk>/', PostView.as_view(), name='post_detail'),
    path('post/new/', AddPostView.as_view(), name='add_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)