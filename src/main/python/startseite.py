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
def aircrafts():
	response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container"><h1>Fl&uuml;ge</h1><table class="table table-hover"><thead><tr><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th></tr></thead>'
	response = response + '<tbody>'
	aircrafts = jsonReader.getAircraftsFromJson()
	for aircraft in aircrafts:
		flightId = aircraft[jsonReader.flightIdLong()]
		startAirport = aircraft[jsonReader.startAirport()]
		targetAirport = aircraft[jsonReader.targetAirport()]
		if flightId <> "" and startAirport <> "" and targetAirport <> "":
			response = response + '<tr>'
			response = response + '<td>' + flightId + '</td>'
			response = response + '<td>' + startAirport + '</td>'
			response = response + '<td>' + targetAirport + '</td>'
			response = response + '</tr>'
	response = response + '</tbody>  </table></div>'
	return response

run(host=getPublicIp(), port=8080)
