from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator

from user.models import User

# Create your models here.
class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  current_balance = models.DecimalField(max_digits=10, default="2000", validators=[MinValueValidator(1)], decimal_places=2)
  account_creation = models.DateTimeField(default=timezone.now)

  @property
  def total_sent_amount(self): #in a day
    return self.sent_transactions.filter(is_today=True).aggregate(models.Sum('transfer_amount'))['transfer_amount__sum'] or 0


