from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('manager','Manager'),
        ('employee','Employee'),   
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    department = models.ForeignKey('departments.Department',on_delete=models.SET_NULL,null=True,blank=True)
    mobile = models.CharField(max_length=15,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default="")
    profile_image = models.ImageField(
        upload_to='profile/',
        null=True,
        blank=True
    )
    original_password = models.CharField(max_length=100, null=True)
    under_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_employees'
    )
    salary = models.PositiveIntegerField(default=0)
    pf_percentage = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=12)

    employee_code = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True)
    
    def __str__(self):
        return self.username


class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    gst_number = models.CharField(max_length=30, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    established_on = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name