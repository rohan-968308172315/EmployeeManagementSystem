from django.db import models
from accounts.models import User
# Create your models here.

class Leave(models.Model):
    
    LEAVE_TYPE = (
    ('Sick Leave','Sick Leave'),
    ('Casual Leave','Casual Leave'),
    ('Emergency Leave','Emergency Leave'),
    ('Medical Leave','Medical Leave'),)

    LEAVE_DURATION = (
    ('Full Day','Full Day'),
    ('First Half','First Half'),
    ('Second Half','Second Half'),)

    leave_type = models.CharField(
    max_length=50,
    choices=LEAVE_TYPE)

    leave_duration = models.CharField(
    max_length=20,
    choices=LEAVE_DURATION,
    default='Full Day')
    STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()
    attachment = models.ImageField(upload_to='leave/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leave_approver'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )