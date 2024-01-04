from django.urls import path, include

from .views import transfer_funds, account_statement


urlpatterns = [
      path('', transfer_funds),
      path('all', account_statement),
]
