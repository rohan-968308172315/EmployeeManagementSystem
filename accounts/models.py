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
    def __str__(self):
        return self.username