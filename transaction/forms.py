from django import forms

from user.models import User

from .models import Transaction

class TransferFundsForm(forms.ModelForm):
    payee = forms.EmailField()
    class Meta:
      model = Transaction
      fields = ['transfer_amount', 'purpose_of_transfer']
