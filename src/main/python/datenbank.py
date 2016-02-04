import MySQLdb

# connect
db = MySQLdb.connect(host="systemintegration.cmavq3o8re9w.us-east-1.rds.amazonaws.com", user="system", passwd="datenbank",
db="flugdaten")

cursor = db.cursor()

# execute SQL select statement
cursor.execute("SELECT * FROM Flugdaten")

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    print "Datensatz:"
    for element in row:
        print element

cursor.execute("INSERT INTO Flugdaten VALUES ('ID', 'StartAirport', 'targetAirport')")
db.commit()

db.close()

