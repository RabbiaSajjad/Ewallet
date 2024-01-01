from django.urls import path, include

from account.views import AccountView


urlpatterns = [
      path('', AccountView.index),
      path('edit', AccountView.edit_account)
]
