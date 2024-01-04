from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from beneficiary.views import BeneficiaryView


urlpatterns = [
  path('add', BeneficiaryView.as_view()),
]
