from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_us, name='about'),
    path('regulamin/', views.regulamin, name='regulamin'),
    path('create_package/', views.create_package, name='create_package'),
    path('pay_package/<int:package_id>/', views.pay_package, name='pay_package'),
    path('package_detail/<int:package_id>/', views.package_detail, name='package_detail'),
]
