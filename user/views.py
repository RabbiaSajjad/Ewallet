from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from inflect import engine

from EWallet.common.base_view import BaseView
from account.models import Account
from account.serializers import AccountSerializer
from user.utils.email_utils import send_email_confirmation

from .models import User
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login


class UserView(BaseView):
  def get(self, request, id=None):
    if id:
      resource=self._find_resource(id)
      return Response({ self._model_name: UserSerializer(resource).data })
    else:
      db_data = self._model.objects.all()
      serialized_data = UserSerializer(db_data, many=True)
      return Response({ engine().plural(self._model_name): serialized_data.data })

  def post(self, request):
    serializer = UserSerializer(data=request.data)  # Pass the data dictionary to the serializer
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Resource saved successfully"})
    else:
      return Response({"message": "Operation failed"})

  def delete(self, request, id):
    try:
      resource=self._find_resource(id)
      resource.delete()
      return Response({"message":"Resource deleted successfully" })
    except ObjectDoesNotExist:
      pass

  def put(self, request, id):
    resource=self._find_resource(id)
    if resource:
      return self._save_resource(UserSerializer(resource,data=request.data, partial=True), request)

  def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            send_email_confirmation(request, user)
             # Send email confirmation
            return render(request, 'verify_email.html')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

  def login_user(request):
    if request.method == 'POST':
      form = UserLoginForm(request, data=request.POST)
      import pdb;
      pdb.set_trace()
      if form.is_valid():
            # Authenticate the user
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
          login(request, user)
          account = Account.objects.get(user=user.pk)
          context = {
          'user': user,
          'account': account,
          }
                # Redirect to the home page
          return render(request,'home_page.html', context)
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

  def verify_email(request):
    return render(request, 'verify_email.html')

  def activate(self, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # import pdb;
        # pdb.set_trace()
        # new_email = request.GET.get('new_email', None)
        # if new_email:
        #   user.email = new_email
        user.save()
        account = AccountSerializer(data={'user': user.pk})  # Pass the data dictionary to the serializer
        if account.is_valid():
          account.save()
        return redirect('account_activation_complete')
    else:
        return HttpResponseBadRequest('Activation link is invalid!')

  def account_activation_complete(request):
    return render(request, 'verification_complete.html')

  def logout(request):
    request.session.flush()
    return redirect('/user/login')

  def home(request):
    return render(request, 'home_page.html')
