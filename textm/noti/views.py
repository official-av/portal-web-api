from django.shortcuts import render
import nexmo
#from djexmo import send_message


# Create your views here.
def message(request):
    client = nexmo.Client(key='66505af0', secret='cltyPLV3jQJQYYwX')
    client.send_message({'from': '919473805008', 'to': '918448161159', 'text': 'Question recieved !! '})
    return render(request,'message.html',{})
