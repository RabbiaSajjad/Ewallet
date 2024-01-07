from django import forms

CONTACT_CHOICES = [
    ('email', 'Email Address'),
    ('contact_number', 'Contact Number'),
    ('cnic', 'CNIC'),
]

class LoadBalanceForm(forms.Form):
    contact_type = forms.ChoiceField(
        label='Select Contact Type',
        choices=CONTACT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    contact_value = forms.CharField(
        label='Contact Value',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    balance_amount = forms.DecimalField(
        label='Balance amount',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_value=0,
    )

    def clean(self):
        cleaned_data = super().clean()
        contact_type = cleaned_data.get('contact_type')
        contact_value = cleaned_data.get('contact_value')
        balance_amount = cleaned_data.get('balance_amount')

        if contact_type == 'email' and not forms.EmailField().clean(contact_value):
            raise forms.ValidationError('Invalid email address.')

        return cleaned_data

