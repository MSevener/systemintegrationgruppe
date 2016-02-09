import data.jsonReader as jsonReader
import data.dataService as dataService
import data.BucketService as bucketService
import string
import time

def getAircraftMainPage():
    response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container">\
    <h1>Fl&uuml;ge</h1> \
    <table class="table table-hover"> \
    <thead><tr><th></th><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th></tr></thead>' \
               '<tbody>'
    aircrafts = dataService.requestAircraftData(False)
    for i in range(0,len(aircrafts) - 1):
        aircraft= aircrafts[i]
        flightId = aircraft[jsonReader.flightId()]
        startAirport = aircraft[jsonReader.startAirport()]
        targetAirport = aircraft[jsonReader.targetAirport()]
        planeTypeCode = aircraft[jsonReader.planeTypeCode()]
        if flightId <> "" and startAirport <> "" and targetAirport <> "":
            response = response + '<tr onclick="location.href= \'aircrafts/' + flightId + '?type=' + planeTypeCode + '\'\">' \
                                  '<td>' + bucketService.getThumbnailImg(planeTypeCode) + ' </td>' \
                                  '<td>' + str(flightId) + ' </td>' \
                                  '<td>' + str(startAirport) + '</td>' \
                                  '<td>' + str(targetAirport) + '</td>' \
                                  '</tr>'
    response = response + '</tbody>  </table></div>'
    return response

def getAircraftsBrbPage():
	data = dataService.getAircraftsBrb()
	
	response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container">\
        <h1>Flugzeuge &uumlber Brandenburg</h1> \
        <table class="table table-hover"> \
        <thead><tr><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th><th>Datum / Zeit</th></tr></thead>' \
                   '<tbody>'

	for row in data:
		response = response + '<tr>' \
                                  '<td>' + str(row[0]) + ' </td>' \
                                  '<td>' + str(row[1]) + '</td>' \
                                  '<td>' + str(row[2]) + '</td>' \
				  '<td>' + str(row[3]) + '</td>' \
                                  '</tr>'


	response = response + '</tbody>  </table></div>'
        return response


def getAircraftDetailPage(aircraftId, planeTypeShort):
    aircraft=jsonReader.getAircraft(aircraftId)
    if aircraft == 0:
        return ""

    flightId = aircraft["flight"]
    planeType = ""
    if "aircraft" in aircraft:
   	 planeType = aircraft["aircraft"]
    startAirportId = ""
    if "from_iata" in aircraft:
         startAirportId = aircraft["from_iata"]
    targetAirportId = ""
    if "to_iata" in aircraft:
         targetAirportId = aircraft["to_iata"]
    startAirportName = ""
    if "from_city" in aircraft:
         startAirportName = aircraft["from_city"]
    targetAirportName = ""
    if "to_city" in aircraft:
         targetAirportName = aircraft["to_city"]
    departureTime = time.localtime(aircraft["departure"])
    departureTime = time.strftime("%d.%m.%Y %H:%M:%S", departureTime)
    arrivalTime = time.localtime(aircraft["arrival"])
    arrivalTime = time.strftime("%d.%m.%Y %H:%M:%S", arrivalTime)
    status = ""
    if "status" in aircraft:   
         status = aircraft["status"]
    airline = ""
    if "airline" in aircraft:
         airline = aircraft["airline"]
    imageURL = ""
    if "image" in aircraft:
         imageURL = aircraft["image"]

    bucketService.getImagePath("src/dummy.jpg", imageURL)

    response = '<!DOCTYPE html>' \
               '<html lang="en">' \
               '<html lang="en">' \
               '<head>  <title>Flugdaten</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1">  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>' \
               '</head>' \
               '<body><div class="container col-md-8"><h1>Flugzeugdaten</h1> \
                <table class="table table-striped"><tbody>' \
              '<tr><td class = "col-md-4"><b>Flugzeugtyp</b></td>' \
              '<td>{8}</td></tr>' \
                '<tr><td class = "col-md-4"><b>Airline</b></td>' \
              '<td>{7}</td></tr>' \
              '</tbody></table></div><div class = "col-md-4">' \
              '<img src = "{9}" width = "400px" height = "250px" />' \
              '</div>' \
              '<div class="container col-md-12"><h1>Reisedaten</h1><table class="table table-striped"><tbody>' \
              '<tr><td><b>Startflughafen</b></td>' \
              '<td>{5} ({6})</td></tr>' \
                '<tr><td><b>Abflugzeit</b></td>' \
              '<td>{4}</td></tr>' \
              '<tr><td><b>Zielflughafen</b></td>' \
              '<td>{2} ({3})</td></tr>' \
                '<tr><td class = "col-md-4"><b>Ankunftszeit</b></td>' \
              '<td>{1}</td></tr>' \
                '<tr><td><b>Status</b></td>' \
                '<td>{0}</td></tr>' \
                '</tbody></table></div>' \
                '</html>'.format(str(status),str(arrivalTime).encode("utf-8"),str(targetAirportName).encode("utf-8"),str(targetAirportId).encode("utf-8"),str(departureTime).encode("utf-8"),str(startAirportName).encode("utf-8"),str(startAirportId).encode("utf-8"),str(airline).encode("utf-8"),str(planeType).encode("utf-8"),bucketService.getImagePath(planeTypeShort, imageURL))
    return response
