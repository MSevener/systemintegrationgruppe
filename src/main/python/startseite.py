from bottle import route, run, template
import urllib
import jsonReader

def getPublicIp():
	ip = urllib.urlopen('http://ip.42.pl/raw').read()
	return ip

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/aircrafts')
def showAircrafts():
	response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container"><h1>Fl&uuml;ge</h1><table class="table table-hover"><thead><tr><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th></tr></thead>'
	response = response + '<tbody>'
	aircrafts = jsonReader.getAircraftsFromJson()
	for aircraft in aircrafts:
		flightId = aircraft[jsonReader.flightIdLong()]
		startAirport = aircraft[jsonReader.startAirport()]
		targetAirport = aircraft[jsonReader.targetAirport()]
		if flightId <> "" and startAirport <> "" and targetAirport <> "":
			response = response + '<tr onclick="location.href= \'aircrafts/' + flightId + '\'\">'
			response = response + '<td>' + flightId + ' </td>'
			response = response + '<td>' + startAirport + '</td>'
			response = response + '<td>' + targetAirport + '</td>'
			response = response + '</tr>'
	response = response + '</tbody>  </table></div>'
	return response


@route('/aircrafts/<aircraftId>')
def showDetails(aircraftId):
	aircraft=jsonReader.getAircraft(aircraftId)
	print aircraft
	if aircraft == 0:
		return ""
	flightId = aircraft[jsonReader.flightIdLong()]
	planeId = aircraft[jsonReader.planeId()]
	planeType = aircraft[jsonReader.planeTypeCode()]
	startAirport = aircraft[jsonReader.startAirport()]
	targetAirport = aircraft[jsonReader.targetAirport()]
	latitude = aircraft[jsonReader.latitude()]
	longitude = aircraft[jsonReader.longitude()]
	address = jsonReader.getAddress(latitude, longitude)
	speed = aircraft[jsonReader.speed()]
	altitude = aircraft[jsonReader.altitude()]
	
	response = '<!DOCTYPE html><html lang="en"><head>  <title>Flugdaten</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1">  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script></head><body><div class="container col-md-8">  <h1>Flugzeugdaten</h1>              <table class="table table-striped">    <tbody>'
	response = response + '<tr><td class = "col-md-4"><b>Flugzeug ID</b></td>'
	response = response + '<td>' + planeId + '</td></tr>'
	response = response + '<tr><td class = "col-md-4"><b>Flugzeugtyp</b></td>'
        response = response + '<td>' + planeType + '</td></tr>'
	response = response + '</tbody></table></div><div class = "col-md-4">'
	response = response + '<img src = "http://content.mycutegraphics.com/graphics/household/radio-cassette-player-music-notes.png" width = "250px" height = "250px" />'
	response = response + '</div>'
	
	response = response + '<div class="container col-md-12"><h1>Reisedaten</h1><table class="table table-striped"><tbody>'
	response = response + '<tr><td><b>Startflughafen</b></td>'
	response = response + '<td>' + startAirport + '</td></tr>'
	response = response + '<tr><td><b>Zielflughafen</b></td>'
        response = response + '<td>' + targetAirport + '</td></tr>'
	response = response + '<tr><td><b>L&auml;ngengrad</b></td>'
        response = response + '<td>' + str(latitude)  + '</td></tr>'
	response = response + '<tr><td><b>Breitengrad</b></td>'
        response = response + '<td>' + str(longitude) + '</td></tr>'
	response = response + '<tr><td><b>Aktuelle Adresse</b></td>'
        response = response + '<td>'
	if address <> 0:
		response = response + address + '</td>'
	response = response + '</tr>'
	response = response + '<tr><td><b>Geschwindigkeit</b></td>'
        response = response + '<td>' + str(speed) + '</td></tr>'
	response = response + '<tr><td><b>H&ouml;he</b></td>'
        response = response + '<td>' + str(altitude) + '</td></tr>'
	response = response + '</tbody></table></div>'
	response = response + '</html>'
	return response








	return flightId

run(host=getPublicIp(), port=8080)
