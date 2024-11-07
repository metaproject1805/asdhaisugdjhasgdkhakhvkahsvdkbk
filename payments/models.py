from django.db import models
from base.utils.validators import file_validation
from cloudinary.models import CloudinaryField

class Payment(models.Model):
  level = models.CharField(max_length=15)
  image = CloudinaryField('image', validators=[file_validation], null=True)
  amount = models.IntegerField(default=0)
  
  def __str__(self) -> str:
    return self.level