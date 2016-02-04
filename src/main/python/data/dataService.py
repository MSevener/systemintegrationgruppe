import sched, time
from threading import Timer

def defineTimer():
    t = Timer(60 * 30, requestAircraftData, ()) #shedule again
    t.daemon = True #for a cleanly interrupt
    t.start()

# Requesting aircraft data
def requestAircraftData():
    defineTimer()
    print "dataService: request data"
    #    aircraftData = jsonReader.getAircraftsFromJson()

def initialize():
    defineTimer()

initialize()