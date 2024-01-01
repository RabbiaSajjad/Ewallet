from django.shortcuts import redirect, render
from requests import Response
from account.forms import EditAccountForm
from account.serializers import AccountSerializer
from django.contrib.auth.decorators import login_required

from EWallet.common.base_view import BaseView
from user.models import User
from user.utils.email_utils import send_email_confirmation

# Create your views here.

@login_required
class AccountView(BaseView):
  def index(request, id=None):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'account_page.html', {'user':user})

  def post(self, request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Resource saved successfully"})
    else:
      return Response({"message": "Operation failed"})

  def edit_account(request):
    user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
      user = User.objects.get(pk=request.user.pk)
      form = EditAccountForm(request.POST, request.FILES, instance=user)
      if form.is_valid():
        if request.user.email != form.cleaned_data['email']:
          send_email_confirmation(request, user)
        form.save(commit=False)

         # Redirect to the account details page after successful update
        return redirect('/account')
    else:
        form = EditAccountForm(initial={
            'full_name': user.full_name,
            'contact': user.contact,
            'address': user.address,
            'cnic': user.cnic,
            'email': user.email,
        })
    return render(request, 'edit_account_page.html', {'user': user, 'form': form})
