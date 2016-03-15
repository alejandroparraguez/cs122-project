from django import forms
import datetime
#Created by Django, class written by us

class infoForm(forms.Form):
    '''
    Creates class infoForm, with fields for start address, destination address,
    number of passengers, and choice of city.
    '''
    startAddress = forms.CharField(label='Start Address', max_length = 500)
    endAddress = forms.CharField(label='End Address', max_length = 500)
    city_choices = (("chicago", u'Chicago'),
                    ("new_york_city", u'New York City'),
                    ("san_francisco", u'San Francisco'))
    city = forms.ChoiceField(label='Choose Your City', choices=city_choices)
    passengers = forms.IntegerField(label='Passengers',max_value=6,min_value=1)
    
