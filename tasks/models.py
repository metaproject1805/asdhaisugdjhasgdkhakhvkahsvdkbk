from django.db import models



class Task(models.Model):
  CATEGORY_CHOICES = [
    ("movie", "movie"),
    ("music", "music"),
    ("thrillers", "thrillers"),
    ("commercial advertisement", "commercial advertisement"),
    ("football", "football"),
  ]
  category = models.CharField( choices=CATEGORY_CHOICES, max_length=50)
  file = models.FileField(upload_to="files")
  watch_count = models.IntegerField(default=0)
  total_watch = models.IntegerField(default=100)
  
  def set_watch_count(self):
    self.watch_count = self.total_watch

  def save(self):
    self.set_watch_count()
    return super().save()
  
  def __str__(self) -> str:
    return self.category