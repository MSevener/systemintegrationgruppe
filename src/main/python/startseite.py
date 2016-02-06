#!/usr/bin/python
from bottle import route, run, template, request
import urllib
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
	planeTypeShort = request.query.get('type')
	return gui.getAircraftDetailPage(aircraftId, planeTypeShort)

run(host=getHostname(), port=8080)
#print getHostname()
