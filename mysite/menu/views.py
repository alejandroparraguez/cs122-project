from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .directions import master
from .forms import infoForm


def get_travel_info(request):
	if request.method == 'POST':
		form = infoForm(request.POST)
		if form.is_valid():
			passengers = form.cleaned_data['passengers']
			start_address = form.cleaned_data['startAddress']
			print(start_address)
			end_address = form.cleaned_data['endAddress']
			print(end_address)
			city = form.cleaned_data['city']
			backend = master(start_address, end_address, passengers, city)
			if backend['valid'] == True: 
				if city == "chicago":
					return render(request, 'menu/thanks.html', backend)
				if city == "san_francisco":
					return render(request, 'menu/thanksSF.html', backend)
				if city == "new_york_city":
					print("Going to NY")
					return render(request, 'menu/thanksNY.html', backend)
			else:
				return render(request, 'menu/error.html')

			
	else:
		form = infoForm()
	return render(request, 'menu/index.html', {'form': form})


def return_directions(request):
	return render(request, 'menu/thanks.html')



