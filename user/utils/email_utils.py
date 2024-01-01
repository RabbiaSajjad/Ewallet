# your_app/utils/email_utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from user.tokens import account_activation_token  # Import your token here

def send_email_confirmation(request, user):
    current_site = get_current_site(request)
    subject = 'Activate your account'
    message = render_to_string('verification_instructions_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[user.email]
    )
    email.content_subtype = 'html'
    email.send()
    return
