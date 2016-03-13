from django import forms
import datetime

# Create your models here.
class infoForm(forms.Form):
    startAddress = forms.CharField(label='Start Address', max_length = 500)
    endAddress = forms.CharField(label='End Address', max_length = 500)
    city_choices = (("chicago", u'Chicago'),
                    ("new_york_city", u'New York City'),
                    ("san_francisco", u'San Francisco'))
    city = forms.ChoiceField(label='Choose Your City', choices=city_choices)
    #city = city.lower()
    passengers = forms.IntegerField(label='Passengers',max_value=6,min_value=1)
    
