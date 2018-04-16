from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.core.mail import send_mail
from django.template.loader import render_to_string
def mail(request):
   msg_plain = render_to_string('email.txt')
   msg_html = render_to_string('email.html')
   from_email =settings.EMAIL_HOST_USER
   to_email = 'anmolvashisthaav@gmail.com'
   send_mail(
    'NOTIFICATION EMAIL',
    msg_plain,
    from_email,
    [to_email],
    html_message=msg_html,
    fail_silently=False
    )
   return render(request, "confirmation.html")
