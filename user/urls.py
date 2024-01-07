from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from user.views import UserView


urlpatterns = [
      path('', UserView.as_view(http_method_names=['post', 'get'])),
      path('<int:id>', UserView.as_view(http_method_names=['put', 'get', 'delete'])),
      path('register', UserView.register),
      path('login', UserView.login_user, name='login'),
      path('logout', UserView.logout, name='logout'),
      path('home', UserView.home),
      path('verify-email', UserView.verify_email),
      path('activate/<str:uidb64>/<token>/', UserView.activate, name='activate'),
      path('account_activation_complete/', UserView.account_activation_complete, name='account_activation_complete'),
      path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
