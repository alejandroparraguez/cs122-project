import requests as req
import json

#start = "5433 South University Avenue, Chicago"
#stop = "Art Institute of Chicago"

key = 'AIzaSyByDOFQN5iEuGMIKF7mO9f79_GqO6ZWM1s'
uber_key = 'NtbAU8JtNKJKqs8IEskwOfBq_pWZvKq0y6bXGLcf'

def read_fare_info(file_name):
	with open(file_name) as data_file:
		fare_info = json.load(data_file)
	return fare_info

def driving_google_req(start,stop):
	url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(start) + '&destination=' + str(stop) + '&key=' + key
	r = req.get(url)
	data = r.json()
	coord = start_end_coord(start, stop, key, data)
	return coord, data
	

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

def calc_cab_fare(mile, num_pass, data, fare_info):
	
	sec = 0
	meters = 0
	for route in data['routes']:
		leg = route['leg']
		duration = leg['duration']
		distance = leg['distance']
		
		sec += duration['value']
		meters += duration['value']

	minutes = float(sec)/60.00
	miles = meters * 0.00062137
	
	base_fare = fare_info['base_fare']
	per_mile = fare_info["per_mile"]
	per_min = fare_info["per_min"]
	first_passenger = fare_info["first_passenger"]
	add_passenger = fare_info["additional_passenger"]
	clean_fee = fare_info["clean_fee"]
	airport_tax = fare_info["airport_tax"]
	
	if num_pass > 1:
		pass_fare = first_passenger + add_passenger * (num_pass - 1)
	else:
		pass_fare = 0
	
	return base + (per_mile * mile) + (per_min * minutes) + pass_fare


def calc_uber(crd, ub_key):
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

	uber_estimates = {}

	for dicti in ub_data['prices']:
		est_key = dicti["display_name"]
		price = dicti["estimate"]
		length = dicti["duration"]
		uber_estimates[est_key] = [length/60, price]

	return uber_estimates	

def calc_transit(start, stop, key, fare_info, travelers):
	url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(start) + '&destination=' + str(stop) + '&mode=transit' + '&key=' + key
	print(url)
	r = req.get(url)
	data = r.json()

	#print("data before: ", data['routes'])
	duration_text = data['routes'][0]['legs'][0]['duration']['text']
	#print("duration after: ", duration_text)
	duration = data['routes'][0]['legs'][0]['duration']['value']
	instructions = []
	transit = []
	for leg in data['routes'][0]['legs'][0]['steps']:
		instructions.append(leg['html_instructions'])
		if 'transit_details' in leg.keys():
			transit.append(leg['transit_details']['line']['vehicle']['type'])
	cost = calc_transit_cost(transit, fare_info)

	print transit

	return [int(duration/60), cost*travelers] #["Total cost: $" + str(int(cost*travlers)), transit]


def calc_transit_cost(transit, fare_info):
	
	total_cost = 0.0
	for vehicle in transit:
		total_cost = total_cost + float(fare_info['transit'][vehicle])
	return total_cost

def master(start, stop, travelers):

	fare_compare = {}
	fare_info = read_fare_info("menu/IL_taxi.json")
	#fare_info = read_fare_info("IL_taxi.json")

	coord, data = driving_google_req(start,stop)

	#fare_compare['taxi'] = calc_cab_fare(file_name, mile, num_pass, data, fare_info)

	#ub_est = calc_uber_price_time(start, stop, key, uber_key, data)
	fare_compare['uber'] = calc_uber(coord, uber_key)
	#fare_compare['uber'] = {'uberX':[4, 6], 'uberXL':[5, 7]}
	fare_compare['taxi'] = [5,3]
	
	#transit = calc_transit(start, stop, key, fare_info, travlers)
	fare_compare['public'] = calc_transit(start, stop, key, fare_info, travelers)
	
	#print(transit)
	return fare_compare

#testing("5433 South University Avenue, Chicago", "Art Institute, Chicago", 5)
fake_directions = {'driving':[5], 'taxi':[5, 10], 'uber':{'uberX':[4, 6], 'uberXL':[5, 7]}, 'public':[4, 11]}
