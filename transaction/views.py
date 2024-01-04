from django.utils import timezone
from django.shortcuts import redirect, render
from django.db.models import Sum

from account.models import Account
from user.models import User
from .forms import TransferFundsForm

# Create your views here.
from .models import Transaction  # Import your Transaction model

def validate_transaction(instance):
  sender = Account.objects.get(pk=instance.sender_id)
  payee = Account.objects.get(pk=instance.payee_id)
  if instance.transfer_amount > sender.current_balance:
    return False
  elif sender is None or payee is None:
    return False
  return True

def update_balance(instance):
  sender = Account.objects.get(pk=instance.sender_id)
  payee = Account.objects.get(pk=instance.payee_id)

  sender.current_balance = sender.current_balance - instance.transfer_amount
  sender.save()

  payee.current_balance = payee.current_balance + instance.transfer_amount
  payee.save()

def transfer_funds(request):
  if request.method == 'POST':
    form = TransferFundsForm(request.POST)
    if form.is_valid():
      form.instance.sender_id = Account.objects.get(user=request.user.pk).pk
      payee_account = User.objects.get(email=form.cleaned_data['payee'])
      form.instance.payee_id = Account.objects.get(user=payee_account.pk).pk
    if validate_transaction(form.instance):
      form.instance.save()
    if surplus_charges(form.instance.sender_id):
      form.instance.transfer_amount += 200
    update_balance(form.instance)

    return render(request, 'transfer_funds.html')

  else:
    form = TransferFundsForm()

  return render(request, 'transfer_funds.html', {'form': form})

def account_statement(request):
  user = request.user.pk
  user_account = Account.objects.get(user=user).pk
  sent_transfers = Transaction.objects.filter(sender_id=user_account)
  received_transfers = Transaction.objects.filter(payee_id=user_account)

  context = {
      'sent_transfers': sent_transfers,
      'received_transfers': received_transfers,
  }

  return render(request, 'account_statement.html', context)

def surplus_charges(sender):
  sent_transactions = Transaction.objects.filter(sender_id=sender)
  if sent_transactions.filter(timestamp__date=timezone.now().date()).aggregate(Sum('transfer_amount'))['transfer_amount__sum'] > 25000:
    return True
  return False
