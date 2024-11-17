from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TAILOR', 'Tailor'),
        ('CUSTOMER', 'Customer'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.user_type}"

class TailorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tailor_profile')
    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Tailor Profile"

class CustomerProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    measurements = models.JSONField(default=dict, blank=True)
    preferred_styles = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Customer Profile"
