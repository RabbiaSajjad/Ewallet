from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from inflect import engine

from EWallet.common.base_view import BaseView
from account.models import Account
from account.serializers import AccountSerializer
from beneficiary.forms import AddBeneficiaryForm
from user.utils.email_utils import send_email_confirmation

from .models import Beneficiary, User
from user.serializers import UserSerializer
from django.shortcuts import render, redirect
from user.forms import UserRegistrationForm, UserLoginForm
from user.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login


class BeneficiaryView(BaseView):
  def add_beneficiary(request):
    import pdb;
    pdb.set_trace()
    if request.method == 'POST':
        form = AddBeneficiaryForm(request.POST, request.FILES)
        if form.is_valid():
          nickname = form.cleaned_data['nickname']
          email = form.cleaned_data['email']

          user = User.objects.get(email=email)
          beneficiary, created = Beneficiary.objects.get_or_create(user=request.user)
          beneficiary.nickname = nickname
          beneficiary.friends.add(user)
          beneficiary.save()
    else:
        form = AddBeneficiaryForm()

    return render(request, 'add_beneficiary.html', {'form': form})

