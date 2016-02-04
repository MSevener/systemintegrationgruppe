import urllib
import json
import jsonFiles

def getAircraftsFromJson():
	flightDataStr = urllib.urlopen('http://krk.data.fr24.com/zones/fcgi/feed.json?array=1')
	flightData = json.load(flightDataStr)
	return flightData["aircraft"]

def getAircraft(searchedAircraft):
	aircrafts = getAircraftsFromJson()
	i = 0
	while aircrafts[i][flightIdLong()] <> searchedAircraft and i < len(aircrafts) -1:
		i = i + 1
	if i < len(aircrafts):
		return aircrafts[i]
	else:
		return 0

def getLocationJson(lat, lng):
	locationStr = urllib.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(lng) + '&sensor=false')
	return json.load(locationStr)

def getAddress(lat, lng):
	location = getLocationJson(lat, lng)
	if location["results"] == []:
		return 0
	else:
		return location["results"][0]["formatted_address"]

def getAirportName(airportId):
	airportArray = jsonFiles.getAirportsJson()
	airports = airportArray["rows"]
	for airport in airports:
		id = airport["iata"]
		if airportId == id:
			return airport["name"]
	return 0

def latitude():
	return 2

def longitude():
	return 3

def planeTypeCode():
	return 9

def planeId():
	return 10

def flightId():
	return 14

def flightIdLong():
	return 17

def startAirport():
	return 12

def targetAirport():
	return 13

def altitude():
	return 5

def speed():
	return 6

def squawk():
	return 7

print getAirportName("AAE")
#print getAirportJson()
