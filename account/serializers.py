from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = Account
    fields = ['id','user','current_balance', 'account_creation']

