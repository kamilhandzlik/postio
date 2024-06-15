from django.shortcuts import render
from .models import UserPackage
# Create your views here.


def homepage(request):
    """View of home page."""
    packages = UserPackage.objects.all()
    return render(request, 'main/homepage.html', {'packages': packages})

