from django.urls import path, include

from user.views import UserView


urlpatterns = [
      path('', UserView.as_view(http_method_names=['post', 'get'])),
      path('<int:id>', UserView.as_view(http_method_names=['put', 'get', 'delete'])),
      path('register', UserView.register),
      path('login', UserView.login),
      path('verify-email', UserView.verify_email),
      path('activate/<str:uidb64>/<token>/', UserView.activate, name='activate'),
      path('account_activation_complete/', UserView.account_activation_complete, name='account_activation_complete'),
]
