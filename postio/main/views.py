from django.shortcuts import render

# Create your views here.
def home(request):
    """Wyświetl stronę główną"""
    return render(request, 'main/base.html', {})