from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from user.utils.email_utils import send_email_confirmation


from user.models import User
from account.forms import EditAccountForm

# Create your views here.

class AccountView(LoginRequiredMixin, APIView):
  def index(request, id=None):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'account_page.html', {'user':user})

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
