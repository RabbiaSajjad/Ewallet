from django import forms
from .models import Beneficiary

class AddBeneficiaryForm(forms.Form):
  nickname = forms.CharField(max_length=255, label='Nickname')
  email = forms.EmailField()
