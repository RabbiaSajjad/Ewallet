from django.urls import path, include

from .views import AdminView
from transaction.views import transfer_funds


urlpatterns = [
      path('', transfer_funds),
      path('list_users', AdminView.display_users)
]
