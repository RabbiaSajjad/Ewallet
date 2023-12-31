from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

from EWallet.settings import DEFAULT_FROM_EMAIL

class User(AbstractBaseUser):
  email = models.EmailField(verbose_name= "email", max_length=60, unique=True)
  username = models.CharField(max_length=30, unique=True)
  last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
  profile_picture = models.ImageField(upload_to="image")
  full_name = models.CharField(max_length=30)
  cnic = models.CharField(max_length=15, unique=True)
  address = models.CharField(max_length=100)
  contact = models.CharField(max_length=20, unique=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False) #If user has activated his account by following the confirmation email

  USERNAME_FIELD = 'username'

  def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
