import time
import jsonReader
import mailSender
import MySQLdb
from threading import Timer
from termcolor import colored

TIMER_SECONDS = 60 * 30 # alle 30min


# Defines a Timer for the next data request
def defineTimer():
    t = Timer(TIMER_SECONDS, requestAircraftData, [True]) #shedule data request again
    t.daemon = True #daemon, for a clean interrupt
    t.start()

# Requesting aircraft data
def requestAircraftData(setTimer):
    print "dataService: requesting aircraft data (setTimer={0})".format(setTimer)
    if setTimer:
        defineTimer()
    aircraftData = jsonReader.getAircraftsFromJson()

    # filter empty flights
    aircraftData = filterData(aircraftData)

    # handle Brandenburg aircrafts (save in DB)
    brbAircrafts = getBrbData(aircraftData)
    saveData(brbAircrafts)

    # check for emergencys
    emergencyCheck(aircraftData)

    return aircraftData

# Filter aircraft data
def filterData(aircraftData):
    filteredAircrafts = [] #instanciate Resultlist
    for aircraft in aircraftData:
        flightId = aircraft[jsonReader.flightId()]
        startAirport = aircraft[jsonReader.startAirport()]
        targetAirport = aircraft[jsonReader.targetAirport()]
        if flightId != "" and startAirport != "" and targetAirport != "":
            filteredAircrafts.append(aircraft)
    print colored("{0} aircrafts found. ({1} omitted -> no data)"\
                  .format(len(aircraftData),len(aircraftData)-len(filteredAircrafts)),\
                  'green')#(len(aircraftData)==1500) if 'green' else 'red')
    return filteredAircrafts

# Check for emergency
def emergencyCheck(aircraftData):
    for aircraft in aircraftData:
        flightId = aircraft[jsonReader.flightId()]
        emg = aircraft[jsonReader.squawk()]
        if emg == 7500 or emg == 7600 or emg ==  7700:
            mailSender.sendEmail(flightId)

# Brandenburg Geolocation-Ranges
# Lat between 53.558497 - 51.361819
# Lng between 14.759853 - 11.265845
LAT_BRB_NORTH = 53.558497
LAT_BRB_SOUTH = 51.361819
LNG_BRB_EAST = 14.759853
LNG_BRB_WEST = 11.265845

# Zip Code Ranges for Brandenburg
# http://www.cebus.ch/de/plz-bundesland.htm
brbZipCodeRanges = [[1941,1998],[3001,3253],[4891,4938],[14401,14715],[14723,16949],
                    [17258,17258],[17261,17291],[17309,17309],[17321,17321],
                    [17326,17326],[17335,17335],[17337,17337],[19307,19357]]

# Check: is in Brandenburg?
def checkIsInBrb(lat, lng):
    # rude filering with geolocations of Brandenburg:
    if not (lat < LAT_BRB_NORTH and lat > LAT_BRB_SOUTH and lng < LNG_BRB_EAST and lng > LNG_BRB_WEST):
        return False
    # Try get location & analyze ZIP Code
    location = jsonReader.getAddress(lat, lng)
    #print location
    try:
        zipAndCity = location.split(",")[1].strip()
        zip = int(zipAndCity.split()[0])
    except:
        # couldnt extract zip code
        print colored("Couldnt extract zip code",'red'), "from location='{0}'".format(location.encode('utf-8'))
        return False
    # check location zipcode is in Brb
    for brbZipRange in brbZipCodeRanges:
        if zip > brbZipRange[0] and zip < brbZipRange[1]:
            print "Aircraft found in {0}".format(location.encode('utf-8'))
            return True #is in Brb
    return False #zipcode not in Brb

# Filter aircraft data for Brandenburg
def getBrbData(aircraftData):
    brbAircrafts = [] #instanciate Resultlist

    for aircraft in aircraftData:
        lat = aircraft[jsonReader.latitude()]
        lng = aircraft[jsonReader.longitude()]
        aircraftIsInBrb = checkIsInBrb(lat, lng)
        if not aircraftIsInBrb:
            continue
        brbAircrafts.append(aircraft)

    print colored("{0} aircrafts found above Brandenburg.".format(len(brbAircrafts)),'green')
    return brbAircrafts

SQL_TABLENAME = 'Flugdaten'
SQL_COLUMN_ID = 'id'
SQL_COLUMN_START = 'startairport'
SQL_COLUMN_TARGET = 'targetairport'
SQL_COLUMN_DATE = 'reg_date'

# Save aircraft data in DB
def saveData(data):
    if len(data) == 0:
        return

    db = MySQLdb.connect(host="systemintegration.cmavq3o8re9w.us-east-1.rds.amazonaws.com", user="system", passwd="datenbank",db="flugdaten")
    cursor = db.cursor()
    cnt = 0

    for brbPlane in data:
        flightId = brbPlane[jsonReader.flightId()]
        startAirport = brbPlane[jsonReader.startAirport()]
        targetAirport = brbPlane[jsonReader.targetAirport()]
        timestamp = int(time.time())
        replaceQuery = "REPLACE INTO {0} SET id='{4}',startairport='{2}',targetairport='{3}',reg_date=FROM_UNIXTIME({1})"\
            .format(SQL_TABLENAME, timestamp, startAirport, targetAirport, flightId)
        cursor.execute(replaceQuery)
        if int(cursor.rowcount)!=-1:
            cnt+=1

    print "{0} aircrafts above Brandenburg saved in DB.".format(cnt)
    db.commit()
    db.close()

def initialize():
    defineTimer()

initialize()
