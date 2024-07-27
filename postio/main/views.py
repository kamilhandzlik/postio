from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, View
from .models import UserPackage
from .forms import UserPackageForm
import qrcode
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'main/homepage.html'


class AboutUsView(TemplateView):
    template_name = 'main/about_us.html'


class RegulaminView(TemplateView):
    template_name = 'main/regulamin.html'


class CreatePackageView(CreateView):
    model = UserPackage
    form_class = UserPackageForm
    template_name = 'main/create_package.html'

    def form_valid(self, form):
        package = form.save(commit=False)
        package.price = self.calculate_price(package.weight, package.width, package.height, package.lenght)
        package.paid = False
        package.status = 'ready_to_ship'
        package.save()
        return redirect('pay_package', package_id=package.package_id)

    def calculate_price(self, weight, width, height, length):
        # Calculating package based upon weight, price and dimensions
        base_price = 10
        weight_factor = weight * 0.5
        size_factor = (width * height * length) * 0.01
        return base_price + weight_factor + size_factor


class PayPackageView(View):
    template_name = 'main/pay_package.html'

    def get(self, request, *args, **kwargs):
        package_id = self.kwargs['package_id']
        package = get_object_or_404(UserPackage, pk=package_id)
        context = {'package': package}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        package_id = self.kwargs['package_id']
        package = get_object_or_404(UserPackage, pk=package_id)
        package.paid = True
        package.status = 'paid'
        package.save()
        return redirect('package_detail', package_id=package.package_id)


class PackageDetailView(DetailView):
    model = UserPackage
    template_name = 'main/package_detail.html'
    context_object_name = 'package'
    pk_url_kwarg = 'package_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = self.get_object()
        qr_code_path = self.generate_qr_code(package)
        context['qr_code_url'] = qr_code_path
        return context

    def generate_qr_code(self, package):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Package ID: {package.package_id}\nStatus: {package.status}\nPrice: {package.price}')
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        qr_code_path = f'media/qr_codes/package_{package.package_id}.png'
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        img.save(qr_code_path)
        return qr_code_path


class EditPackageView(View):
    template_name = 'main/edit_package.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        package_id = self.kwargs['package_id']
        package = get_object_or_404(UserPackage, pk=package_id)
        form = UserPackageForm(instance=package)
        if request.user.groups.filter(name='Dostawca').exists() or request.user.is_superuser:
            context = {'form': form, 'package': package}
            return render(request, self.template_name, context)
        else:
            return HttpResponseForbidden("Nie masz pozwolenia żeby edytować tą paczkę.")

    @method_decorator(login_required)
    def post(self, requset, *args, **kwargs):
        package_id = self.kwargs['package_id']
        package = get_object_or_404(UserPackage, pk=package_id)
        form = UserPackageForm(requset.POST, instance=package)
        if requset.user.groups.filter(name='Dostawca').exist() or requset.user.is_superuser:
            if form.is_valid():
                form.save()
                return redirect('package_detail', package_id=package.package_id)
            else:
                return render(requset, self.template_name, {'form': form, 'package': package})
        else:
            return HttpResponseForbidden("Nie masz pozwolenia żeby edytować tą paczkę.")
