import urllib
import json

def getAircraftsFromJson():
	flightDataStr = urllib.urlopen('http://krk.data.fr24.com/zones/fcgi/feed.json?array=1')
	flightData = json.load(flightDataStr)
	return flightData["aircraft"]

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
