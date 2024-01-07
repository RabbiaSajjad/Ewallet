from transaction.views import transfer_funds
from user.models import User
from .forms import LoadBalanceForm
from transaction.forms import TransferFundsForm

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication



class AdminView(APIView):
  # authentication_classes = [JWTAuthentication]

  def display_users(request):
    users = User.objects.filter(is_staff='f',is_superuser='f')

    return render(request, 'users_list.html', {'users':users})
