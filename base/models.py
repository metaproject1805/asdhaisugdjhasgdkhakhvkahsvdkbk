from django.db import models

class SystemState(models.Model):
    key = models.CharField(max_length=255, unique=True)
    last_run_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.key