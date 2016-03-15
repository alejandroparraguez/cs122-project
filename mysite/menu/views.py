from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .directions import master
from .forms import infoForm
#Created by Django, written by us

def get_travel_info(request):
	'''
	Gets form from request, if valid, sends to backend and renders results page. If parameters are not valid as
	per backend, an error page is rendered. 
	'''
	if request.method == 'POST':
		form = infoForm(request.POST)
		if form.is_valid():
			passengers = form.cleaned_data['passengers']
			start_address = form.cleaned_data['startAddress']
			end_address = form.cleaned_data['endAddress']
			city = form.cleaned_data['city']
			try:
				backend = master(start_address, end_address, passengers, city)
			#Render error page if request to backend fails
			except:
				return render(request, 'menu/error.html')
			#Render error page if backend judges parameters invalid
			if backend['valid'] == True: 
				if city == "chicago":
					return render(request, 'menu/thanks.html', backend)
				if city == "san_francisco":
					return render(request, 'menu/thanksSF.html', backend)
				if city == "new_york_city":
					return render(request, 'menu/thanksNY.html', backend)
			else:
				return render(request, 'menu/error.html')

			
	else:
		form = infoForm()
	return render(request, 'menu/index.html', {'form': form})


def return_directions(request):
	'''
	Renders results page.
	'''
	return render(request, 'menu/thanks.html')

