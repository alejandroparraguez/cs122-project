from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404

#from .models import choiceQuestion, addressQuestion
#from directions import testing
from .forms import infoForm

fake_directions = {'driving':[5], 'taxi':[5, 10], 'uber':{'uberX':[4, 6], 'uberXL':[5, 7]}, 'public':[4, 11]}

def get_travel_info(request):
	if request.method == 'POST':
		form = infoForm(request.POST)
		print('HERE!')
		if form.is_valid():
			passengers = form.cleaned_data['passengers']
			start_address = form.cleaned_data['startAddress']
			end_address = form.cleaned_data['endAddress']
			#backend = testing(start_address, end_address, passengers)
			#print(start_address)
			#return HttpResponseRedirect('/menu/thanks/')
			#return HttpResponse(test)
			return render(request, 'menu/thanks.html', fake_directions)#{"fake_directions": fake_directions})

	else:
		form = infoForm()
	return render(request, 'menu/index.html', {'form': form})

def return_directions(directions):
	return render({"directions": directions}, 'menu/thanks.html')



