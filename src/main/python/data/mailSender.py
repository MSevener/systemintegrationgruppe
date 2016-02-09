from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def sendEmail(aircraftID):
	sender = "tino.maik.max@sysintproj.de"
	to = "si@thomas-preuss.de"
	text = "Das Flugzeug mit der ID "
	text = text + aircraftID + " hat einen Notfall."
	message = MIMEText(text)
	message['Subject'] = "Notfall"
	message['From'] = sender
	message['To'] = to
		
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(message.as_string())
