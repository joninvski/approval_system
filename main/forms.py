from django import forms
from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
     class Meta:
         model = Order
         fields = ['number']

MY_CHOICES = (
    ('y', 'Accept'),
    ('-', 'Pending'),
    ('n', 'Reject'),
)

class MyForm(forms.Form):
    my_choice_field = forms.ChoiceField(choices=MY_CHOICES)
    order_id = forms.CharField(widget=forms.HiddenInput())
