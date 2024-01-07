from django.urls import path, include

from .views import transfer_funds, account_statement

app_name = 'transaction'

urlpatterns = [
      path('', transfer_funds),
      path('statement/<int:user>/', account_statement, name='account_statement'),
]
