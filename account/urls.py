from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from account.views import AccountView


urlpatterns = [
      path('', AccountView.index),
      path('edit', AccountView.edit_account),
]
