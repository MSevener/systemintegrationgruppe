#!/usr/bin/python
from bottle import route, run, template
import os
import subprocess
import gui

def getHostname():
	hostprocess = subprocess.Popen(['ec2metadata', '--public-hostname'], stdout=subprocess.PIPE)
	hostname = hostprocess.stdout.read()
	hostname = hostname.decode('UTF-8')
	hostname = hostname.strip()
	return hostname

@route('/hello/<name>')
def index(name):
	return template('<b>Hello {{name}}</b>!', name=name)

@route('/aircrafts')
def showAircrafts():
	return gui.getAircraftMainPage()


@route('/aircrafts/<aircraftId>')
def showDetails(aircraftId):
	return gui.getAircraftDetailPage(aircraftId)

run(host=getHostname(), port=8080)
#print getHostname()
