from django.db import models
from base.utils.validators import file_validation


class Investment(models.Model):
  DURATION_CHOICES = [
    ("7 Days", "7 Days"),
    ("30 Days", "30 Days"),
    ("60 Days", "60 Days"),
    ("90 Days", "90 Days"),
    ("120 Days", "120 Days"),
    ("360 Days", "360 Days"),
    ("1080 Days", "1080 Days"),
  ]
  PAYMENT_STATUS_CHOICES = [
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Pending", "Pending"),
  ]
  duration = models.CharField(choices=DURATION_CHOICES, max_length=20)
  
  daily_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending")
  wallet_email = models.EmailField(null=True, blank=True)
  wallet_id = models.CharField(max_length=20, null=True, blank=True)
  days_remaining =  models.IntegerField(default=0)
  payment_slip = models.ImageField('image', upload_to="investments", validators=[file_validation], null=True)
  price = models.IntegerField()
  level = models.IntegerField(default=0, blank=True)
  is_withdrawable = models.BooleanField(default= False)
  
  
  def investment_manager(self):
    if self.duration == "7 Days":
      self.daily_earning = 1.00
      self.days_remaining = 7
      self.level=1
    elif self.duration == "30 Days":
      self.daily_earning = 1.3
      self.days_remaining = 30
      self.level=2
    elif self.duration == "60 Days":
      self.earning = 2.00
      self.daily_earning = 60
      self.level=3
    elif self.duration == "90 Days":
      self.daily_earning = 4.00
      self.days_remaining = 90
      self.level=4
    elif self.duration == "120 Days":
      self.daily_earning = 5.00
      self.days_remaining = 120.00
      self.level=5
    elif self.duration == "360 Days":
      self.daily_earning = 8.00
      self.days_remaining = 360
      self.level=6
    elif self.duration == "1080 Days":
      self.daily_earning = 12.00
      self.days_remaining = 1080
      self.level=7

    self.save()
   
    
  def __str__(self) -> str:
    return self.payment_status