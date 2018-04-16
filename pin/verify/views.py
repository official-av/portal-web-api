from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from .forms import OrderForm
from django.contrib.auth import settings
import nexmo
import random

# Create your views here.
def _get_pin(length=5):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]


#def _verify_pin(mobile_number, pin):
#    """ Verify a PIN is correct """
#    return pin == cache.get(mobile_number)


def ajax_send_pin(request):

       """ Sends SMS PIN to the specified number """

       mobile_number = request.POST.get('mobile_number', "")
       if not mobile_number:
            return HttpResponse("No mobile number", mimetype='text/plain', status=403)

       pin = _get_pin()

       # store the PIN in the cache for later verification.
       #cache.set(mobile_number, pin, 24*3600) # valid for 24 hrs

      #client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
      #message = client.messages.create(
                        #body="%s" % pin,
                        #to=mobile_number,
                        #from_=settings.TWILIO_FROM_NUMBER,
                    #)
       client = nexmo.Client(key='66505af0', secret='cltyPLV3jQJQYYwX')
       client.send_message({'from': '919473805008', 'to': mobile_number, 'text': pin})

       return HttpResponse("Message is send")

#def process_order(request):
#    """ Process orders made via web form and verified by SMS PIN. """

#    form = OrderForm(request.POST or None)
#    if request.method == "POST":
#        print(form)
#        if form.is_valid():

#            pin = int(request.POST.get("pin", "0"))
#            mobile_number = request.POST.get("mobile_number", "")

#            if _verify_pin(mobile_number, pin):
#               form.save()
#               render('transaction_complete')
#            else:
#               messages.error(request, "Invalid PIN!")

#        else:
#            return render(request,'verify/check.html')



#    return render(request,'verify/order.html',{'form': form})
