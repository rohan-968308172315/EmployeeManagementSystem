from django.db import models
from accounts.models import User

# Create your models here.

class Attendance(models.Model):

    STATUS_CHOICES = (
        ('Present','Present'),
        ('Absent','Absent'),
        ('Half Day','Half Day'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_marked'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user','attendance_date')