from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from user.utils.email_utils import send_email_confirmation
from user.views import update_email
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



from user.models import User
from account.forms import EditAccountForm

# Create your views here.

class AccountView(LoginRequiredMixin, APIView):
  authentication_classes = [JWTAuthentication]

  def index(request, id=None):
    try:
        user = get_object_or_404(User, pk=request.user.pk)
        return render(request, 'account_page.html', {'user': user})
    except User.DoesNotExist:
        return render(request, 'user_not_found.html')

  def edit_account(request):
    try:
      user = User.objects.get(pk=request.user.pk)

      if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        form = EditAccountForm(request.POST, request.FILES, instance=user)
        import pdb;
        pdb.set_trace()
        if form.is_valid():
          if request.user.email != form.cleaned_data['email']:
            send_email_confirmation(request, user)
            # form.save(commit=False)
          else:
             form.save()

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

    except User.DoesNotExist:
        return render(request, 'user_not_found.html')
