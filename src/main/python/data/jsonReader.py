import urllib
import json
import jsonFiles
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
# Constants
# URLs
URL_FR24_KRK = 'http://krk.data.fr24.com/zones/fcgi/feed.json'
URL_FR24_ARN = 'http://arn.data.fr24.com/zones/fcgi/feed.json'
# Params
PARAM_FLIGHT = 'flight'
PARAM_ARRAY = 'array'


def getAircraftsFromJson():
	flightDataURL = '{0}?{1}={2}'.format(URL_FR24_KRK, PARAM_ARRAY, '1')
	print "request json: {0}".format(flightDataURL)
	flightData = json.load(urllib.urlopen(flightDataURL))
	return flightData["aircraft"]

def getAircraft(searchedAircraft):
	flightDataURL = '{0}?{1}={2}'.format(URL_FR24_KRK, PARAM_FLIGHT, searchedAircraft)
	print "request json: {0}".format(flightDataURL)
	flightData = json.load(urllib.urlopen(flightDataURL))
	return flightData

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

def sendEmail(aircraftID):
	sender = "jo@gmail.com"
	to = "rothe.maik93@gmail.com"
	text = "Das Flugzeug mit der ID "
	text = text + aircraftID + " hat einen Notfall"
	message = MIMEText(text)
	message['Subject'] = "Notfall"
	message['From'] = sender
	message['To'] = to
		
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(message.as_string())

	
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

#print getAirportName("AAE")
#print getAirportJson()
