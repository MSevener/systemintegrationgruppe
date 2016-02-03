import os 
import subprocess 
import string 

def getHostName():
	hostprocess = subprocess.Popen(['ec2metadata', '--public-hostname'], stdout=subprocess.PIPE)
	hostname = hostprocess.stdout.read()
	hostname = hostname.decode('UTF-8')
	return hostname
#print(getHostName())
