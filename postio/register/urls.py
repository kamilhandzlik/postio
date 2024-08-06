from django.contrib import admin
from django.urls import path, include
from .views import RegistrationView, CustomLoginView, CustomLogoutView, PasswordChangeAjaxView, ProfileView
from django.conf.urls.static import static
from django.conf import settings
#test commit
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RegistrationView.as_view(), name='register'),
    path('', include("main.urls")),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change_ajax/', PasswordChangeAjaxView.as_view, name='password_change_ajax')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
