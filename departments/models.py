from django.db import models

# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20)
    description = models.TextField()
    status  = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)