import requests as req
import json
import pprint
import math
from bs4 import BeautifulSoup

key = 'AIzaSyByDOFQN5iEuGMIKF7mO9f79_GqO6ZWM1s'
uber_key = 'NtbAU8JtNKJKqs8IEskwOfBq_pWZvKq0y6bXGLcf'
map_key ='AIzaSyDrUubINuulSxDYp5rmG-NuvR-Zo_oLrmY'
geocode_key = 'AIzaSyAiIUbZYNYCg7cuj73HxaXaSYJyeq_rFdM'

def read_fare_info(file_name):
	with open(file_name) as data_file:
		fare_info = json.load(data_file)
	return fare_info

def google_req(start, stop, mode):
	url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(start)+ '&destination=' +str(stop)+ '&mode=' +mode+ '&key=' +key
	print(url)
	r = req.get(url)
	data = r.json()
	pprint.pprint(data)
	coord = start_end_coord(start, stop, key, data)

	embed_map = "https://www.google.com/maps/embed/v1/directions?key=" +map_key+ "&origin=" +str(start)+ "&destination="+str(stop) + '&mode=' +mode
	return coord, data, embed_map
	

def start_end_coord(start, stop, key, data):
	#Start coordinates
	route0 = data['routes'][0]
	leg0 = route0['legs'][0]
	step0 = leg0['steps'][0]
	start_loc0 = step0['start_location']

	start_lat = start_loc0['lat']
	start_long = start_loc0['lng']
	
	#End coordinates
	last_route = data['routes'][-1]
	last_leg = last_route['legs'][-1]
	last_step = last_leg['steps'][-1]
	last_end_loc = last_step['end_location']

	end_lat = last_end_loc['lat']
	end_long = last_end_loc['lng']
	
	return [start_lat, start_long, end_lat, end_long]

def calc_route(num_pass, data, fare_info, mode):
	
	meters = 0
	time = data['routes'][0]['legs'][0]['duration']['text']
	sec = data['routes'][0]['legs'][0]['duration']['value']
	minutes = sec/60
	
	instructions = []
	for step in data['routes'][0]['legs'][0]['steps']:
		#soup = BeautifulSoup(step['html_instructions'], 'html.parser')
		#instruction_step_html = soup.
		instructions.append(step['html_instructions'])
		meters += step['distance']['value']

	miles = meters * 0.00062137
	
	fare = 0
	if mode == 'driving':
		base = float(fare_info['taxi']['base_fare'])
		per_mile = float(fare_info['taxi']["per_mile"])
		per_min = float(fare_info['taxi']["per_min"])
		first_passenger = float(fare_info['taxi']["first_passenger"])
		add_passenger = float(fare_info['taxi']["additional_passenger"])

		if num_pass > 1:
			pass_fare = first_passenger + add_passenger * (num_pass - 1)
		else:
			pass_fare = 0

		fare = base + (per_mile * miles) + (per_min * minutes) + pass_fare
	
	if mode == 'bicycling':
		fare = float(fare_info['divvy']['base_fare'])
		second_thirty = float(fare_info['divvy']['second_thirty'])
		third_thirty = float(fare_info['divvy']['third_thirty'])
		next_thirty = float(fare_info['divvy']['next_thirty'])
		time_chunks = math.ceil(minutes / 30)
		if time_chunks > 1:
			fare += second_thirty
		if time_chunks > 2:
			fare += third_thirty
		if time_chunks > 3:
			fare += (time_chunks - 3) * next_thirty
		fare = fare * num_pass

	return [int(minutes), "{0:.2f}".format(round(fare,2)), instructions]
	
def nearest_divvy(place):
	google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+str(place)+'&key=' +str(geocode_key)
	r = req.get(google_url)
	address_data = r.json()
	start_lat  = address_data['results'][0]['geometry']['location']['lat']
	start_long = address_data['results'][0]['geometry']['location']['lng']

	divvy_url = 'http://shrouded-beach-2183.herokuapp.com/stations/nearby?'
	first_station_url = divvy_url+ '&lat=' +str(start_lat)+ '&lon=' +str(start_long)+ '&max_stations=1'
	r = req.get(first_station_url)
	station_data = r.json()
	pprint.pprint(station_data)
	coord = station_data[0]['geometry']['coordinates']
	return coord

def calc_divvy(start, stop, num_pass, fare_info):

	divvy1 = nearest_divvy(start)
	#print("divvy1", divvy1)
	divvy1_loc = str(divvy1[1])+','+str(divvy1[0])
	#print("divvy1_loc", divvy1_loc)
	divvy2 = nearest_divvy(stop)
	divvy2_loc = str(divvy2[1])+','+str(divvy2[0])

	coord1, data1, walk1_map = google_req(start, divvy1_loc, "walking")
	[t1, c1, i1] = calc_route(num_pass, data1, None, 'walking')

	bike_coord, bike_data, bike_map = google_req(divvy1_loc, divvy2_loc, "bicycling")
	[bike_t, bike_c, bike_i] = calc_route(num_pass, bike_data, fare_info, 'bicycling')

	coord3, data3, walk2_map = google_req(divvy2_loc, stop, "walking")
	[t3, c3, i3] = calc_route(num_pass, data3, None, 'walking')

	total_t = t1 + t3 + bike_t

	return [total_t, bike_c, i1 + bike_i + i3], bike_map, walk1_map, walk2_map


def calc_transit(start, stop, fare_info, travelers, mode):
	url = "https://maps.googleapis.com/maps/api/directions/json?origin=" +str(start)+ '&destination=' +str(stop)+ '&mode=' +mode+ '&key=' +key
	r = req.get(url)
	data = r.json()

	duration_text = data['routes'][0]['legs'][0]['duration']['text']
	duration = data['routes'][0]['legs'][0]['duration']['value']
	
	instructions = []
	transit = []
	for leg in data['routes'][0]['legs'][0]['steps']:
		instructions.append(leg['html_instructions'])
		if 'transit_details' in leg.keys():
			transit.append(leg['transit_details']['line']['vehicle']['type'])

	cost = calc_transit_cost(transit, fare_info)

	transit_map = "https://www.google.com/maps/embed/v1/directions?key=" +map_key+ "&origin=" +str(start)+ "&destination="+str(stop) + '&mode=transit'

	return [int(duration/60), cost*travelers, instructions], transit_map 


def calc_transit_cost(transit, fare_info):
	
	total_cost = 0.0
	for vehicle in transit:
		total_cost = total_cost + float(fare_info['transit'][vehicle])
	return total_cost


def calc_uber(crd, ub_key, passengers):
	url = 'https://api.uber.com/v1/estimates/price'

	parameters = {
    'server_token': ub_key,
    'start_latitude': crd[0],
    'start_longitude': crd[1],
    'end_latitude': crd[2],
    'end_longitude': crd[3]
	}

	response = req.get(url, params=parameters)
	ub_data = response.json()

	pass_less_5 = ['UberBLACK','uberX','uberESPANOL','UberSELECT']


	uber_estimates = {}
	if passengers > 4:
		for dicti in ub_data['prices']:
			est_key = dicti["display_name"]
			price = dicti["estimate"]
			length = dicti["duration"]
			if est_key in pass_less_5:
				pass	
			else:
				uber_estimates[est_key] = [length/60, price]
	else:
		for dicti in ub_data['prices']:
			est_key = dicti["display_name"]
			price = dicti["estimate"]
			length = dicti["duration"]
			uber_estimates[est_key] = [length/60, price]

	return uber_estimates	


def master(start, stop, travelers):

	fare_compare = {}
	map_urls = []
	fare_info = read_fare_info("menu/IL_taxi.json")
	#fare_info = read_fare_info("IL_taxi.json")

	coord, driving_data, fare_compare['driving_map'] = google_req(start, stop, 'driving')
	fare_compare['taxi'] = calc_route(travelers, driving_data, fare_info, 'driving')

	fare_compare['uber'] = calc_uber(coord, uber_key, travelers)
	
	public = 'transit&transit_routing_preference=fewer_transfers'
	fare_compare['public'], fare_compare['transit_map'] = calc_transit(start, stop, fare_info, travelers, public)
	#fare_compare['public'], fare_compare['transit_map'] = 

	fare_compare['divvy'], fare_compare['bike_map'], fare_compare['walk1_map'], fare_compare['walk2_map'] = calc_divvy(start, stop, travelers, fare_info)
	#print(fare_compare['divvy'], divvy_i)
	#print(fare_compare['taxi'][2][0]))

	return fare_compare

master("5433 South University Avenue, Chicago", "Art Institute, Chicago", 5)
