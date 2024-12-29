from django.db import models
from base.utils.validators import file_validation
from cloudinary.models import CloudinaryField


class Packages(models.Model):
  LEVEL_CHOICES = [
    ("Level 1", "Level 1"),
    ("Level 2", "Level 2"),
    ("Level 3", "Level 3"),
    ("Level 4", "Level 4"),
    ("Level 5", "Level 5"),
    ("Level 6", "Level 6"),
    ("Level 7", "Level 7"),
    ("Level 8", "Level 8"),
    ("Level 9", "Level 9"),
    ("Level 10", "Level 10"),
    ("Level 11", "Level 11"),
  ]
  PAYMENT_STATUS_CHOICES = [
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Pending", "Pending"),
  ]
  level = models.CharField(choices=LEVEL_CHOICES, max_length=20)
  payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending")
  earning_per_task = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  payment_slip = CloudinaryField('image', validators=[file_validation], null=True)
  wallet_email = models.EmailField(null=True, blank=True)
  wallet_id = models.CharField(max_length=200, null=True, blank=True)
  price = models.IntegerField()
  daily_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  days_remaining =  models.IntegerField(default=0)
  max_number_of_task =  models.IntegerField(default=0)
  max_upgrade = models.BooleanField(default=False)
  is_withdrawable = models.BooleanField(default= False)
  layer = models.IntegerField(default=0)
  
  # @property
  # def max_number_of_task(self):
  #   return round(self.daily_earning/self.earning_per_task, 2)
  
  def investment_manager(self):
    
    if self.level == "Level 1":
      self.earning_per_task = 0.65
      self.daily_earning = 1.3
      self.days_remaining = 90
      self.max_number_of_task = 2
      self.layer = 1
    if self.level == "Level 2":
      self.earning_per_task = 0.675
      self.daily_earning = 2.7
      self.days_remaining = 90
      self.max_number_of_task = 4
      self.layer = 2
    elif self.level == "Level 3":
      self.earning_per_task = 0.78
      self.daily_earning = 3.9
      self.days_remaining = 90
      self.max_number_of_task = 5
      self.layer = 3
    elif self.level == "Level 4":
      self.earning_per_task = 1
      self.daily_earning = 8
      self.days_remaining = 90
      self.max_number_of_task = 8
      self.layer = 4
    elif self.level == "Level 5":
      self.earning_per_task = 1.125
      self.daily_earning = 13.5
      self.days_remaining = 90
      self.max_number_of_task = 12
      self.layer = 5
    elif self.level == "Level 6":
      self.earning_per_task = 2.0385
      self.daily_earning = 26.5005
      self.days_remaining = 90
      self.layer = 6
    elif self.level == "Level 7":
      self.earning_per_task = 2
      self.daily_earning = 40
      self.days_remaining = 90
      self.max_number_of_task = 13
      self.layer = 7
    elif self.level == "Level 8":
      self.earning_per_task = 2.12
      self.daily_earning = 53
      self.days_remaining = 90
      self.max_number_of_task = 20
      self.layer = 8
    # elif self.level == "Level 8":
    #   self.earning_per_task = 5.00
    #   self.daily_earning = 40
    #   self.days_remaining = 90
    #   self.layer = 7
    # elif self.level == "Level 9":
    #   self.earning_per_task = 6.00
    #   self.daily_earning = 50
    #   self.days_remaining = 90
    #   self.layer = 8
    # elif self.level == "Level 10":
    #   self.earning_per_task = 8.00
    #   self.daily_earning = 50
    #   self.days_remaining = 90
    #   self.layer = 9
    # elif self.level == "Level 11":
    #   self.earning_per_task = 10.00
    #   self.daily_earning = 50
    #   self.days_remaining = 90
    #   self.layer = 10
    #   self.max_upgrade = True

    self.save()
    
    
  def __str__(self) -> str:
    return self.payment_status