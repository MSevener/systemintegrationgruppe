import data.jsonReader as jsonReader
import data.dataService as dataService
import string

def getAircraftMainPage():
    response = '<html><head>  <title>Aircrafts</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head><body><div class="container"><h1>Fl&uuml;ge</h1><table class="table table-hover"><thead><tr><th>FlugID</th><th>Startflughafen</th><th>Zielflughafen</th></tr></thead>' \
               '<tbody>'
    aircrafts = dataService.requestAircraftData(False)
    for aircraft in aircrafts:
        flightId = aircraft[jsonReader.flightIdLong()]
        startAirport = aircraft[jsonReader.startAirport()]
        targetAirport = aircraft[jsonReader.targetAirport()]
        if flightId <> "" and startAirport <> "" and targetAirport <> "":
            response = response + '<tr onclick="location.href= \'aircrafts/' + flightId + '\'\">' \
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

    flightId = aircraft[jsonReader.flightIdLong()]
    planeId = aircraft[jsonReader.planeId()]
    planeType = aircraft[jsonReader.planeTypeCode()]
    startAirportId = aircraft[jsonReader.startAirport()]
    targetAirportId = aircraft[jsonReader.targetAirport()]
    startAirportName = jsonReader.getAirportName(startAirportId)
    targetAirportName = jsonReader.getAirportName(targetAirportId)
    latitude = aircraft[jsonReader.latitude()]
    longitude = aircraft[jsonReader.longitude()]
    address = jsonReader.getAddress(latitude, longitude)
    speed = aircraft[jsonReader.speed()]
    altitude = aircraft[jsonReader.altitude()]

    response = '<!DOCTYPE html>' \
               '<html lang="en">' \
               '<head>  <title>Flugdaten</title>  <meta charset="utf-8">  <meta name="viewport" content="width=device-width, initial-scale=1">  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>' \
               '</head>' \
               '<body><div class="container col-md-8">  <h1>Flugzeugdaten</h1>              <table class="table table-striped">    <tbody>' \
              '<tr><td class = "col-md-4"><b>Flugzeug ID</b></td>' \
              '<td>' + str(planeId)+ '</td></tr>' \
              '<tr><td class = "col-md-4"><b>Flugzeugtyp</b></td>' \
              '<td>' + str(planeType) + '</td></tr>' \
              '</tbody></table></div><div class = "col-md-4">' \
              '<img src = "https://s3.amazonaws.com/mandelbrotm/Flugzeug.jpg" width = "400px" height = "250px" />' \
              '</div>' \
              '<div class="container col-md-12"><h1>Reisedaten</h1><table class="table table-striped"><tbody>' \
              '<tr><td><b>Startflughafen</b></td>' \
              '<td>' + str(startAirportName) + ' (' + str(startAirportId) + ')</td></tr>' \
              '<tr><td><b>Zielflughafen</b></td>' \
              '<td>' + str(targetAirportName) + ' (' + str(targetAirportId) + ')</td></tr>' \
              '<tr><td><b>Breitengrad</b></td>' \
              '<td>' + str(latitude)  + '</td></tr>' \
              '<tr><td><b>L&auml;ngengrad</b></td>' \
              '<td>' + str(longitude) + '</td></tr>' \
              '<tr><td><b>Aktuelle Position</b></td>' \
              '<td>'
    if address <> 0:
        response = response + str(address) + '</td>'
    response = response + '</tr>' \
                          '<tr><td><b>Geschwindigkeit</b>' \
                          '</td>' \
                          '<td>' + str(speed) + '</td></tr>' \
                          '<tr><td><b>H&ouml;he</b></td>' \
                          '<td>' + str(altitude) + '</td></tr>' \
                          '</tbody></table></div>' \
                          '</html>'
    return response