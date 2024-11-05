from django.db import models
from base.utils.validators import file_validation

class Payment(models.Model):
  level = models.CharField(max_length=15)
  image = models.ImageField('image', upload_to="payments", validators=[file_validation], null=True)
  amount = models.IntegerField(default=0)
  
  def __str__(self) -> str:
    return self.level