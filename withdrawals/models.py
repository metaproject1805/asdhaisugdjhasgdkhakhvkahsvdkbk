from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Withdrawal(models.Model):
  PAYMENT_STATUS_CHOICES = [
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
    ("Pending", "Pending"),
  ]
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="eligible_for_withdrawal" )
  wallet_address = models.CharField(max_length=200, null=True, blank=True)
  payment_status = models.CharField(max_length=200, choices=PAYMENT_STATUS_CHOICES, default="Pending")
  wallet_email = models.EmailField(null=True, blank=True)
  wallet_id = models.CharField(max_length=200, null=True, blank=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)