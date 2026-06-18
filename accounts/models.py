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
    mobile = models.CharField(max_length=15,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username