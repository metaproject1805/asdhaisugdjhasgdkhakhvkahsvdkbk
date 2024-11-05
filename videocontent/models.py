from unicodedata import category
from django.db import models

# Create your models here.
class VideoContent(models.Model):
  CATEGORY_CHOICES = [
    ("Ads", "Ads"),
  ]
  
  category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Ads")
  video = models.FileField(upload_to="videos")