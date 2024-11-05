from django.urls import path
from .views import InvestmentCreateView

urlpatterns = [
    path("investment-create/", InvestmentCreateView.as_view(), name="investment-create-view"),
]
