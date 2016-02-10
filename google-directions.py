import requests as req
import json

start = 'Houston, TX'
stop = 'Chicago, IL'
key = 'AIzaSyByDOFQN5iEuGMIKF7mO9f79_GqO6ZWM1s'

url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(start) + '&destination=' + str(stop) + '&key=' + key
r = req.get(url)
data = r.json()

route0 = data['routes'][0]
leg0 = route0['legs'][0]
step0 = leg0['steps'][0]
start_loc0 = step0['start_location']

start_lat = start_loc0['lat']
start_long = start_loc0['lng']

last_route = data['routes'][-1]
last_leg = last_route['legs'][-1]
last_step = last_leg['steps'][-1]
last_end_loc = last_step['end_location']

end_lat = last_end_loc['lat']
end_long = last_end_loc['lng']

def calc_cab_fare(file, min, mile, num_pass):
	with open() as data_file:
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

sec = 0
meters = 0
for route in data['routes']:
	leg = route['leg']
	duration = leg['duration']
	distance = leg['distance']
	
	sec += duration['value']
	meters += duration['value']

min = float(sec)/60.00

calc_cab_fare('IL_taxi.json', min, miles, num_pass)
print(
