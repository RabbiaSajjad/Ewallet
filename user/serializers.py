from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import authenticate
from user.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','username','email', 'full_name', 'password', 'cnic', 'address', 'contact']


class UserLoginSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        """Get user token."""
        user = User.objects.get(email=obj.email)

        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    class Meta:
        model = User
        fields = ['id','username', 'password', 'tokens']

    def validate(self, request):
        data = request.POST
        """Validate and return user login."""
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(request=request, username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')

        return user
