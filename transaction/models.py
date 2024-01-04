from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator

from account.models import Account

# Create your models here.
class Transaction(models.Model):
  sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sent_transactions")
  payee = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="received_transactions")
  transfer_amount = models.DecimalField(max_digits=10, validators=[MinValueValidator(1)], decimal_places=2)
  purpose_of_transfer = models.CharField(max_length=100)
  timestamp = models.DateTimeField(default=timezone.now)
