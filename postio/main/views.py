from django.shortcuts import render

# Create your views here.


def homepage(request):
    """View of home page."""
    return render(request, 'main/homepage.html')

