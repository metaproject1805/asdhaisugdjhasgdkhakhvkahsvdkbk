from django.urls import path
from .views import PaymentListCreateView

urlpatterns = [
    path('payment-list', PaymentListCreateView.as_view(), name="payment-list-view" )
]
