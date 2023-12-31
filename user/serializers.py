from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from user.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','username','email', 'full_name', 'password', 'cnic', 'address', 'contact']

