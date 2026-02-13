# models.py في تطبيق payments
from django.db import models
from django.contrib.auth.models import User
from locations.models import SportsFieldLocation


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")
    field = models.ForeignKey(SportsFieldLocation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment for {self.user} - {self.status}"
