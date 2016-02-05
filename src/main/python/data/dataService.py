import sched, time
import jsonReader
from threading import Timer

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
    analyzeData(aircraftData)
    return aircraftData

# Analyze aircraft data
def analyzeData(data):
    print "analyze data"
    return 0

def initialize():
    defineTimer()

initialize()