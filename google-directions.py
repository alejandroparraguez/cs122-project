import requests as req
import json

<<<<<<< HEAD
start = 'Houston, TX'
stop = 'Chicago, IL'

#test Uber
address_orig  = "5433 South University Avenue"
address_dest = "Art Institute of Chicago"
=======
#test Uber
start  = "5433 South University Avenue, Chicago"
stop = "Pilsen, Chicago"
>>>>>>> 1500972a260f7200f3c7ed25574e299f4eed6919

key = 'AIzaSyByDOFQN5iEuGMIKF7mO9f79_GqO6ZWM1s'
uber_key = 'NtbAU8JtNKJKqs8IEskwOfBq_pWZvKq0y6bXGLcf'

url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(start) + '&destination=' + str(stop) + '&key=' + key
r = req.get(url)
data = r.json()

def start_end_coord(start, stop, key):
	
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
	
	return start_lat, start_long, end_lat, end_long

def calc_cab_fare(file, min, mile, num_pass):
	with open(file) as data_file:
		data = json.load(data_file)
	base_fare = data['base_fare']
	per_mile = data["per_mile"]
	per_min = data["per_min"]
	first_passenger = data["first_passenger"]
	add_passenger = data["additional_passenger"]
	
	clean_fee = data["clean_fee"]
	airport_tax = data["airport_tax"]
	
	if num_pass > 1:
		pass_fare = first_passenger + add_passenger * (num_pass - 1)
	else:
		pass_fare = 0
	
	return base + (per_mile * mile) + (per_min * min) + pass_fare
"""
sec = 0
meters = 0
for route in data['routes']:
	leg = route['leg']
	duration = leg['duration']
	distance = leg['distance']
	
	sec += duration['value']
	meters += duration['value']

min = float(sec)/60.00
miles = meters * 0.00062137

calc_cab_fare('IL_taxi.json', min, miles, num_pass)
"""
def calc_uber_price_time(strt,stp,goog_key,ub_key):
	url = 'https://api.uber.com/v1/estimates/price'
	[st_lat,st_lon,end_lat,end_lon] = start_end_coord(strt, stp, goog_key)

<<<<<<< HEAD
	print(st_lat)
	print(st_lon)
	print(end_lat)
	print(end_lon)

=======
>>>>>>> 1500972a260f7200f3c7ed25574e299f4eed6919
	parameters = {
    'server_token': ub_key,
    'start_latitude': st_lat,
    'start_longitude': st_lon,
    'end_latitude': end_lat,
    'end_longitude': end_lon
	}

	response = req.get(url, params=parameters)
	data = response.json()

	uber_estimates = {}
<<<<<<< HEAD
	print(data)
=======
>>>>>>> 1500972a260f7200f3c7ed25574e299f4eed6919

	for dicti in data['prices']:
		est_key = dicti["display_name"]
		uber_estimates[est_key] = {}
		price = dicti["estimate"]
		length = dicti["duration"]
		uber_estimates[est_key]["fare"] = price
		uber_estimates[est_key]["time"] = length

	return uber_estimates		

<<<<<<< HEAD

ub = calc_uber_price_time(address_orig,address_dest,key,uber_key)

=======
<<<<<<< HEAD

ub = calc_uber_price_time(start,stop,key,uber_key)
print(ub)
=======
if __name__ == "__main__":
	ub = calc_uber_price_time(address_orig,address_dest,key,uber_key)
	print(ub)

>>>>>>> 66bb9ccb1d4f952b388f2af6c5d66f9fbded1945
>>>>>>> 1500972a260f7200f3c7ed25574e299f4eed6919

