import data.jsonReader as jsonReader
import data.dataService as dataService
import string
import time

def getAircraftMainPage():
    response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container">\
    <h1>Fl&uuml;ge</h1> \
    <table class="table table-hover"> \
    <thead><tr><th></th><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th></tr></thead>' \
               '<tbody>'
    aircrafts = dataService.requestAircraftData(False)
    for aircraft in aircrafts:
        flightId = aircraft[jsonReader.flightId()]
        startAirport = aircraft[jsonReader.startAirport()]
        targetAirport = aircraft[jsonReader.targetAirport()]
        if flightId <> "" and startAirport <> "" and targetAirport <> "":
            response = response + '<tr onclick="location.href= \'aircrafts/' + flightId + '\'\">' \
                                  '<td>' + "<img src = "" />" + ' </td>' \
                                  '<td>' + str(flightId) + ' </td>' \
                                  '<td>' + str(startAirport) + '</td>' \
                                  '<td>' + str(targetAirport) + '</td>' \
                                  '</tr>'
    response = response + '</tbody>  </table></div>'
    return response

def getAircraftDetailPage(aircraftId):
    aircraft=jsonReader.getAircraft(aircraftId)
    print aircraft
    if aircraft == 0:
        return ""

    flightId = aircraft["flight"]
    planeType = aircraft["aircraft"]
    startAirportId = aircraft["from_iata"]
    targetAirportId = aircraft["to_iata"]
    startAirportName = aircraft["from_city"]
    targetAirportName = aircraft["to_city"]
    departureTime = time.localtime(aircraft["departure"])
    departureTime = time.strftime("%d.%m.%Y %H:%M:%S", departureTime)
    arrivalTime = time.localtime(aircraft["arrival"])
    arrivalTime = time.strftime("%d.%m.%Y %H:%M:%S", arrivalTime)
    status = aircraft["status"]
    airline = aircraft["airline"]

    response = '<!DOCTYPE html>' \
               '<html lang="en">' \
               '<html lang="en">' \
               '<head>  <title>Flugdaten</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1">  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>' \
               '</head>' \
               '<body><div class="container col-md-8">  <h1>Flugzeugdaten</h1> \
                <table class="table table-striped"><tbody>' \
              '<tr><td class = "col-md-4"><b>Flugzeugtyp</b></td>' \
              '<td>' + str(planeType).encode("utf-8") + '</td></tr>' \
                '<tr><td class = "col-md-4"><b>Airline</b></td>' \
              '<td>' + str(airline).encode("utf-8")+ '</td></tr>' \
              '</tbody></table></div><div class = "col-md-4">' \
              '<img src = "https://s3.amazonaws.com/mandelbrotm/Flugzeug.jpg" width = "400px" height = "250px" />' \
              '</div>' \
              '<div class="container col-md-12"><h1>Reisedaten</h1><table class="table table-striped"><tbody>' \
              '<tr><td><b>Startflughafen</b></td>' \
              '<td>' + str(startAirportName).encode("utf-8") + ' (' + str(startAirportId).encode("utf-8") + ')</td></tr>' \
                '<tr><td><b>Abflugzeit</b></td>' \
              '<td>' + str(departureTime).encode("utf-8")+ '</td></tr>' \
              '<tr><td><b>Zielflughafen</b></td>' \
              '<td>' + str(targetAirportName).encode("utf-8") + ' (' + str(targetAirportId).encode("utf-8") + ')</td></tr>' \
                '<tr><td class = "col-md-4"><b>Ankunftszeit</b></td>' \
              '<td>' + str(arrivalTime).encode("utf-8")+ '</td></tr>' \
                '<tr><td><b>Status</b></td>' \
                '<td>' + str(status).encode("utf-8") + '</td></tr>' \
                '</tbody></table></div>' \
                '</html>'
    return response