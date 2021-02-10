#span_nulls.py
#mike byrne
#sets the cn_substat and cn_feeder fields where they are null
#To use, replace bracketed database, host, username, and password under variables



#variables and importing
import os
from subprocess import call
import psycopg2
import time
now = time.localtime(time.time())
# print " start time: ", time.asctime(now)
# print "	begin: " + (__file__)

#
#******************************************************
#						VARIABLES
#******************************************************
#
#connection
myDB =  "[database]" # "tn_grant" #fcc
myHost = "[hostname]"
myPort = "5432"
myUser = "[username]"
myPWord = "[password]"
myConn = "dbname=" + myDB + " host=" + myHost + " port=" + myPort + " user=" + myUser + " password=" + myPWord
FNULL = open(os.devnull, 'w')

#schema/prefix/workorder/projection
sch = "data" #"fcc" #"form_477_201712"

#tables
#input 
spanTB = "electric_span"

#constants
searchDist = "100000"

#
#******************************************************
#						FUNCTIONS 
#******************************************************
#	
#loop through to make sure all span substat and feeder values are non null
def driveLoop(aField):
	driveCur = conn.cursor()
	driveSQL =  "SELECT gid "
	driveSQL = driveSQL + "FROM " + sch + "." + spanTB + ", "
	driveSQL = driveSQL + "(SELECT geom FROM " + sch + "." + spanTB + " "
	driveSQL = driveSQL + "WHERE " + aField + " IS NOT NULL) as not_null "
	driveSQL = driveSQL + "WHERE " + aField + " IS NULL "
	driveSQL = driveSQL + "AND ST_DWithin(" + spanTB + ".geom, not_null.geom, " + searchDist + ") "
	# driveSQL = driveSQL + "LIMIT 1 "
	driveSQL = driveSQL + "; "
	# print (driveSQL)
	# SELECT gid FROM data.span, 
	#		(SELECT geom FROM data.span WHERE cn_substat IS NOT NULL) as not_null 
	#	WHERE cn_substat IS NULL 
	#	AND ST_DWithin(span.geom, not_null.geom, 1) 
	#	LIMIT 1 
	#	;
	driveCur.execute(driveSQL)
	for row in driveCur:
		aGid = str(row[0])
		fieldVal = returnVal(aGid, aField)
		updValue(aField, fieldVal, aGid)

	driveCur.close()

#return the real value for this field
def returnVal(someGid, someField):
	myVal = 0
	mySQL = "SELECT " + someField + " "
	mySQL = mySQL + "FROM " + sch + "." + spanTB + ", "
	mySQL = mySQL + "(SELECT geom FROM " + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE gid = " + someGid + ") as is_null "
	mySQL = mySQL + "WHERE " + someField + " IS NOT NULL "
	mySQL = mySQL + "AND ST_DWithin(" + spanTB + ".geom, is_null.geom, " + searchDist + ") "
	mySQL = mySQL + "LIMIT 1 "
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT cn_substat FROM data.span, 
	#		(SELECT geom FROM data.span WHERE gid = 121932) as is_null 
	#	WHERE cn_substat IS NOT NULL 
	#	AND ST_DWithin(span.geom, is_null.geom, 1) 
	#	LIMIT 1 
	#	; 
	aCur.execute(mySQL)
	for row	 in aCur:
		myVal = str(row[0])
	return(myVal)


#update the field
def updValue(someField, someVal, someGid):
	updSQL = "UPDATE " + sch + "." + spanTB + " " 
	updSQL = updSQL + "SET " + someField + "= '" + someVal + "' " 
	updSQL = updSQL + "WHERE gid =" + someGid + " "
	updSQL = updSQL + "; "
	updSQL = updSQL + "COMMIT; " 
	# print (updSQL)
	# UPDATE data.span 
	#	SET cn_substat= '1' 
	#	WHERE gid =121931 
	#	; 
	#	COMMIT;
	updCur.execute(updSQL)

#return the number of null records in this field
def returnNullCount(someField):
	theCount = 0
	mySQL = "SELECT COUNT(*) "
	mySQL = mySQL + "FROM " + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE " + someField + " IS NULL "
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT COUNT(*) 
	#	FROM data.span 
	#	WHERE cn_substat IS NULL 

	aCur.execute(mySQL)
	for row in aCur:
		theCount = row[0]
		print (theCount)

	return(theCount)

#perform the vaccum
def myVacuum():
	vConn = psycopg2.connect(myConn)
	#aCur
	aCur = vConn.cursor()
	old_isolation_level = vConn.isolation_level
	vConn.set_isolation_level(0)
	print("			vaccuming: " + sch + "." + spanTB)
	mySQL = "VACUUM ANALYZE " + sch + "." + spanTB + "; "
	aCur.execute(mySQL)
	vConn.set_isolation_level(old_isolation_level)
	#clean up
	aCur.close()





#
#******************************************************
#						MAIN 
#******************************************************
#	
conn = psycopg2.connect(myConn)
#a select cursor
aCur = conn.cursor()
#updCuror
updCur = conn.cursor()

fieldList = ["cn_substat" , "cn_feeder"]
for theField in fieldList:
	recs = returnNullCount(theField)
	prevRecs = recs + 1
	while prevRecs > recs:
		prevRecs = recs
		driveLoop(theField)
		recs = returnNullCount(theField)
	myVacuum()
#clean up
aCur.close()
updCur.close()

#end
#print "		finished: " + (__file__)
now = time.localtime(time.time())
#print "end time:", time.asctime(now)
