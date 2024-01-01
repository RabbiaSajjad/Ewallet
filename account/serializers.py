from rest_framework import serializers

from account.models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = Account
    fields = ['id','user','current_balance', 'account_creation']
