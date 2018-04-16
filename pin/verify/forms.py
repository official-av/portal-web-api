from django import forms

class OrderForm(forms.Form):
    mobile_number= forms.CharField(max_length=10)
    PIN = forms.CharField(max_length=5)
