from django import forms
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class infoForm(forms.Form):
	startAddress = forms.CharField(label='Start Address', max_length = 500)
	endAddress = forms.CharField(label='End Address', max_length = 500)
	passengers = forms.IntegerField(label='Passengers')