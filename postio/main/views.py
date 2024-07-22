from django.shortcuts import render, redirect, get_object_or_404
from .models import UserPackage
from .forms import UserPackageForm


# Create your views here.


def homepage(request):
    """View of home page."""
    packages = UserPackage.objects.all()
    return render(request, 'main/homepage.html', )


def about_us(request):
    return render(request, 'main/about_us.html')


def regulamin(request):
    return render(request, 'main/regulamin.html')


def create_package(request):
    if request.method == 'POST':
        form = UserPackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.price = calculate_price(package.weight, package.width, package.height, package.lenght)
            package.paid = False
            package.status = 'ready_to_ship'
            package.save()
            return redirect('pay_package', package_id=package.package_id)

    else:
        form = UserPackageForm()
    return render(request, 'main/create_package.html', {'form': form})


def pay_package(request, package_id):
    package = get_object_or_404(UserPackage, pk=package_id)
    if request.method == 'POST':
        package.paid = True
        package.status = 'paid'
        package.save()
        return redirect('package_detail', package_id=package.package_id)
    return render(request, 'main/pay_package.html', {'package': package})


def package_detail(request, package_id):
    package_id = get_object_or_404(UserPackage, pk=package_id)
    return render(request, 'main/pay_package.html', {'package': package_id})


def calculate_price(weight, wigth, height, length):
    # Calculating package based upon weight, price and dimensions
    base_price = 10
    weight_factor = weight * 0.5
    size_factor = (wigth * height * length) * 0.01
    return base_price + weight_factor + size_factor
