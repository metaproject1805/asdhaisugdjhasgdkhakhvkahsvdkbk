from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from packages.models import Packages
from investment.models import Investment
from tasks.models import Task



class UserNotification(models.Model):
    TYPE_CHOICES=[
        ('Error', 'Error'),
        ('Success', 'Success'),
        ('Info', 'Info'),
        ('Warning', 'Warning'),
    ] 
    type = models.CharField(choices=TYPE_CHOICES, max_length=15, blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    read = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password = None, **extra_fields): # -> 'User':
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have a username')
        
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Profile(AbstractUser):
    active_ref = models.ManyToManyField("self", blank=True)
    pending_ref = models.ManyToManyField("self", blank=True)    
    username = models.CharField(verbose_name='Username', null=True, unique=True, max_length=50)
    ref_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="user_ref_by")
    email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
    notification = models.ManyToManyField(UserNotification, blank=True)
    ref_code = models.CharField(max_length=50, blank=True)
    security_phase = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    partnership_level = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    weekly_salary = models.IntegerField(default=0)
    phase_active = models.BooleanField(default=False)
    active_package = models.ForeignKey(Packages, on_delete=models.SET_NULL, null=True, blank=True)
    investment = models.ForeignKey(Investment, on_delete=models.SET_NULL, null=True, blank=True)    
    security_phase_1 = models.CharField(max_length=15, blank=True)
    security_phase_2 = models.CharField(max_length=15, blank=True)
    security_phase_3 = models.CharField(max_length=15, blank=True)
    security_phase_4 = models.CharField(max_length=15, blank=True)
    security_phase_5 = models.CharField(max_length=15, blank=True)
    security_phase_6 = models.CharField(max_length=15, blank=True)
    video_watched = models.ManyToManyField(Task, blank=True)
    video_watched_count = models.IntegerField(default=0)
    ref_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    investment_accumulation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    object=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username}"
    
    def get_recommended_profiles(self):
        pass
    
    def save(self, *args, **kwargs):
        if self.ref_code == "":
            self.ref_code = self.username
        super().save(*args, **kwargs)
    
    def upgrade_partnership_level(self):
        if self.active_down_line.count() == 200:
            self.partnership_level += 1
            self.weekly_salary = 25
            self.save()
        
        if self.active_down_line.count() == 400:
            self.partnership_level += 1
            self.weekly_salary = 50
            self.save()
        
        if self.active_down_line.count() == 600:
            self.partnership_level += 1
            self.weekly_salary = 75
            self.save()
        
        if self.active_down_line.count() == 800:
            self.partnership_level += 1
            self.weekly_salary = 100
            self.save()
        
        if self.active_down_line.count() == 1000:
            self.partnership_level += 1
            self.weekly_salary = 250
            self.save()
            