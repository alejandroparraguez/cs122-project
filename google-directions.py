import requests as req
import json


start = 'Houston, TX'
stop = 'Chicago, IL'
key = 'AIzaSyByDOFQN5iEuGMIKF7mO9f79_GqO6ZWM1s'

#mode = 

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

print('start lat', start_lat)
print('start long', start_long)
print('end lat', end_lat)
print('end long', end_long)

