from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_us, name='about'),
    path('regulamin/' , views.regulamin, name='regulamin')
]