from django.db import models

# Create your models here.
from django.db import models
from user.models import User

class Beneficiary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='beneficiary_friends', symmetrical=False)
    nickname = models.CharField(max_length=255)

