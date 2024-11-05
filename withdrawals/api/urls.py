from django.urls import path
from .views import CreateWithdrawalView

urlpatterns = [
  path("withdrawal-create/", CreateWithdrawalView.as_view(), name="create_withdrawal_view")
]