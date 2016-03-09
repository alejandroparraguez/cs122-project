from django import forms
import datetime

# Create your models here.
class infoForm(forms.Form):
	startAddress = forms.CharField(label='Start Address', max_length = 500)
	endAddress = forms.CharField(label='End Address', max_length = 500)
	passengers = forms.IntegerField(label='Passengers',max_value=6,min_value=1)