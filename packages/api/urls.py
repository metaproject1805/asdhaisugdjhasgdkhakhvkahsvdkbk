from django.urls import path
from .views import PackageCreateView

urlpatterns = [
    path("package-create/", PackageCreateView.as_view(), name="package-create-view"),
]
