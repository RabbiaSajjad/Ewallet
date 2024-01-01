from django import forms

from user.models import User
class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'contact', 'profile_picture',
                  'address', 'cnic', 'email']

    def clean_cnic(self):
      cnic = self.cleaned_data['cnic']
      existing_user = User.objects.filter(cnic=cnic).exclude(pk=self.instance.id).first()
      if existing_user is not None:
          raise forms.ValidationError('CNIC already exists for another user.')
      return cnic

    def clean_contact(self):
      contact = self.cleaned_data['contact']
      import pdb;
      pdb.set_trace()
      existing_user = User.objects.filter(contact=contact).exclude(pk=self.instance.id).first()
      if existing_user is not None:
          raise forms.ValidationError('Contact already exists for another user.')
      return contact
