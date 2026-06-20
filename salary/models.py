from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User

class Salarytbl(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    month = models.IntegerField()
    year = models.IntegerField()

    total_working_days = models.IntegerField()

    present_days = models.IntegerField()

    half_days = models.IntegerField()

    paid_leaves = models.IntegerField(
        default=0
    )

    absent_days = models.IntegerField()

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    pf_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.month:02d}/{self.year}"