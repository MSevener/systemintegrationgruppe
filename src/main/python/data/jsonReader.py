import urllib2
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
URL_PLANE = 'http://data.flightradar24.com/_external/planedata_json.1.4.php'
URL_GEONAMES_SUBDIVISION = 'http://api.geonames.org/countrySubdivisionJSON'

# Params
PARAM_FLIGHT = 'f'
PARAM_ARRAY = 'array'
FORMAT = 'format'


def getAircraftsFromJson():
	flightDataURL = '{0}?{1}={2}'.format(URL_FR24_KRK, PARAM_ARRAY, '1')
	print "request json: {0}".format(flightDataURL)
	flightData = json.load(urllib2.urlopen(flightDataURL))
	return flightData["aircraft"]

def getAircraft(searchedAircraft):
	flightDataURL = '{0}?{1}={2}&{3}={4}'.format(URL_PLANE,PARAM_FLIGHT,searchedAircraft,FORMAT,2)
	print "request json: {0}".format(flightDataURL)
	#req = urllib.request.Request(flightDataURL, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
	#print urllib2.urlopen(urllib2.Request(flightDataURL, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
	flightData = json.load(urllib2.urlopen(urllib2.Request(flightDataURL, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})))
	return flightData

def getCountrySubdivision(lat, lng):
	serviceURL = '{0}?lat={1}&lng={2}&username=demo'.format(URL_GEONAMES_SUBDIVISION, lat, lng)
	result = json.load(urllib.urlopen(serviceURL))
	return result

def getLocationJson(lat, lng):
	locationStr = urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(lng) + '&sensor=false')
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
	return 0

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
#print getAircraft("8bbad3a")
