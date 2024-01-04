from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from .models import Beneficiary, User
from beneficiary.forms import AddBeneficiaryForm

class BeneficiaryView(LoginRequiredMixin, APIView):
  def post(self, request):
    if request.method == 'POST':
        form = AddBeneficiaryForm(request.POST, request.FILES)
        if form.is_valid():
          nickname = form.cleaned_data['nickname']
          email = form.cleaned_data['email']

          user = User.objects.get(email=email)
          beneficiary, created = Beneficiary.objects.get_or_create(user=request.user)
          beneficiary.nickname = nickname
          beneficiary.friends.add(user)
          beneficiary.save()


    return render(request, 'add_beneficiary.html', {'form': form})

  def get(self, request):
    form = AddBeneficiaryForm()
    return render(request, 'add_beneficiary.html', {'form': form})
