from django.urls import path
from .views import HomePageView, AboutUsView, RegulaminView, CreatePackageView, PayPackageView, PackageDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('regulamin/', RegulaminView.as_view(), name='regulamin'),
    path('create_package/', CreatePackageView.as_view(), name='create_package'),
    path('pay_package/<int:package_id>/', PayPackageView.as_view(), name='pay_package'),
    path('package_detail/<int:package_id>/', PackageDetailView.as_view(), name='package_detail'),
]
