from django.contrib import admin
from django.urls import path, include
from home_page.views import logout_views, HomeView, LoginView, RegistrationView, AccountView, RedactionAccountView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('logout/', logout_views),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('home/',HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),
    path('redaction/', RedactionAccountView.as_view(), name='redaction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)