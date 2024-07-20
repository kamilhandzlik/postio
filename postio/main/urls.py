from django.urls import path
from . import views
from .views import create_package, pay_package, package_detail

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_us, name='about'),
    path('regulamin/', views.regulamin, name='regulamin'),
    path('create_package/', create_package, name='create_package'),
    path('pay_package/<int:package_id>/', pay_package, name='pay_package'),
    path('package_detail/<int:package_id>/', package_detail, name='package_detail'),
]
