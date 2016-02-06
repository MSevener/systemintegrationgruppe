import time
import jsonReader
import mailSender
import MySQLdb
from threading import Timer

TIMER_SECONDS = 60 * 30 # alle 30min

LAT_BRB_NORTH = 53.558497
LAT_BRB_SOUTH = 51.361819
LNG_BRB_EAST = 14.759853
LNG_BRB_WEST = 11.265845

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

    # handle Brandenburg aircrafts (save in DB)
    brbAircrafts = getBrbData(aircraftData)
    saveData(brbAircrafts)

    # check for emergencys
    emergencyCheck(aircraftData)

    return aircraftData


#Check for emergency
def emergencyCheck(aircraftData):
	for aircraft in aircraftData:
		flightId = aircraft[jsonReader.flightId()]
		emg = aircraft[jsonReader.squawk()]
		if emg == 7500 or emg == 7600 or emg ==  7700:
			mailSender.sendEmail(flightId)


# Filter aircraft data for Brandenburg
def getBrbData(aircraftData):
    brbAircrafts = [] #instanciate Resultlist

    for aircraft in aircraftData:
        lat = aircraft[jsonReader.latitude()]
        lng = aircraft[jsonReader.longitude()]
        # rude filering with geolocations of Brandenburg:
        # Lat between 53.558497 - 51.361819    # Lng between 14.759853 - 11.265845
        aircraftIsInBrb = lat < LAT_BRB_NORTH and lat > LAT_BRB_SOUTH and lng < LNG_BRB_EAST and lng > LNG_BRB_WEST
        if not aircraftIsInBrb:
            continue
        print aircraft
        brbAircrafts.append(aircraft)

    # check detailed location
    location = jsonReader.getCountrySubdivision(lat, lng)
    print location
    print "{0} aircrafts found above Brandenburg.".format(len(brbAircrafts))
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
    for brbPlane in data:
        flightId = brbPlane[jsonReader.flightId()]
        startAirport = brbPlane[jsonReader.startAirport()]
        targetAirport = brbPlane[jsonReader.targetAirport()]
        timestamp = int(time.time())
	#getQuery = "SELECT * FROM {0} WHERE id = '{1}'".format(SQL_TABLENAME, flightId) 
	#updateQuery = "UPDATE {0} SET reg_date='{1}',startairport='{2}',targetairport='{3}' WHERE id = '{4}'".format(SQL_TABLENAME, timestamp, startAirport, targetAirport, flightId)
        #insertQuery = "INSERT INTO {4} VALUES ('{0}', '{1}', '{2}', {3})".format(flightId, startAirport, targetAirport, timestamp, SQL_TABLENAME)
	replaceQuery = "REPLACE INTO {0} SET id='{4}',startairport='{2}',targetairport='{3}',reg_date=FROM_UNIXTIME({1})".format(SQL_TABLENAME, timestamp, startAirport, targetAirport, flightId)
	print replaceQuery
	#cursor.execute(getQuery)
	#data = cursor.fetchall()
	#if len(data) == 0:
        	#print insertQuery
	#else:
		#print updateQuery
#        cursor.execute("INSERT INTO Flugdaten VALUES (brbPlane Id, 'StartAirport', 'targetAirport')")
	cursor.execute(replaceQuery)

    print "{0} aircrafts above Brandenburg detected.".format(int(cursor.rowcount))
    db.commit()
    db.close()

def initialize():
    defineTimer()

initialize()
