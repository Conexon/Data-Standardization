#urban_analysis.py
#mike byrne
#makes metrics about availablilty in urban blocks



#variables and importing
import os
from subprocess import call
import psycopg2
import time
now = time.localtime(time.time())
print ("start time:", time.asctime(now))
print ("	begin: " + (__file__))

#
#******************************************************
#						VARIABLES
#******************************************************
#
#connection
myDB = "standardize" # "tn_grant" #fcc
myHost = "Conexon-design-1.ckdkui5rb8xx.us-east-1.rds.amazonaws.com"
myPort = "5432"
myUser = "conexondataprocess"
myPWord = "conexondataprocess123!" 
myConn = "dbname=" + myDB + " host=" + myHost + " port=" + myPort + " user=" + myUser + " password=" + myPWord
FNULL = open(os.devnull, 'w')


#schema/prefix/workorder/projection
sch = "cooscurry" #"fcc" #"form_477_201712"

#tables
#input 
spanTB = "electric_span"
meterTB = "meter"
subTb = "substation"


conn = psycopg2.connect(myConn)
#a select cursor
aCur = conn.cursor()
#updCuror
updCur = conn.cursor()
####################################
#########functions
def driveLoop():
	driveCur = conn.cursor()
	driveSQL = "SELECT cn_substat, cn_feeder "
	driveSQL = driveSQL + 	"FROM " + sch + "." + spanTB + " "
	driveSQL = driveSQL + "GROUP BY cn_substat, cn_feeder "
	driveSQL = driveSQL + "ORDER BY cn_substat, cn_feeder"
	# print (driveSQL)
	# SELECT cn_substat, cn_feeder 
	#	FROM data.span 
	#	GROUP BY cn_substat, cn_feeder 
	#	ORDER BY cn_substat, cn_feeder

	print ('sub_feeder,substation_name,substation#,feeder#,status,primary_overhead,primary_underground,secondary_overhead,secondary_underground,total_primary,meters,density')
	driveCur.execute(driveSQL)
	for driveRow in driveCur:
		aSub = driveRow[0]
		aFeed = driveRow[1]
		# print (aSub, aFeed)
		subName = returnSubName(aSub)
		status = returnStatus
		# print (subName)
		primary_overhead = returnSpanLength(aSub, aFeed,'1')
		primary_underground = returnSpanLength(aSub, aFeed,'3')
		secondary_overhead = returnSpanLength(aSub, aFeed, '2')
		secondary_underground = returnSpanLength(aSub, aFeed, '4')
		# distro_ring = returnRingLength(aSub, aFeed, '1')
		# aerial = returnSpanLength(aSub, aFeed, 'A')
		# a_miles = round(aerial / 5280,2)
		# # print (aerial)
		# ug = returnSpanLength(aSub, aFeed, 'U')
		# ug_miles = round(ug / 5280,2)
		total_primary = round(primary_overhead + primary_underground,2)
		# print (ug)
		meters = returnMeters(aSub, aFeed)
		density = round(meters/total_primary)
		# print (meters)

		print (aSub + "-" + aFeed,subName,aSub,aFeed,status,primary_overhead,primary_underground,secondary_overhead,secondary_underground,total_primary,meters,density)
		
	driveCur.close()

#return the number of meters:
def returnMeters(mySub, myFeed):
	aSQL = "SELECT COUNT(distinct gid) "
	aSQL = aSQL + "FROM " + sch + "." + meterTB + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND cn_feeder = '" + myFeed + "' "
	aSQL = aSQL + "; "
	# print (aSQL) 
	# SELECT COUNT(distinct gid) 
	#	FROM data.consumers 
	#	WHERE cn_substat = '19' 
	#	AND cn_feeder = 'B224' ;
	count = 0
	aCur.execute(aSQL)
	for row in aCur:
		aCount = row[0]
		if aCount is not None:
			count = aCount
	return(count)

#return the substaiton name
def returnSubName(mySub):
	aSQL = "SELECT subname "
	aSQL = aSQL + "FROM " + sch + "." + subTb + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "; "
	# print (aSQL)
	# SELECT subname 
	#	FROM data.substations 
	#	WHERE cn_substat = '19' ;
	Sub = "someName"
	aCur.execute(aSQL)
	for row in aCur:
		aSub = row[0]
		if aSub is not None:
			Sub = aSub
	return(Sub)

#function for return aerial
def returnSpanLength(mySub, myFeed, subType):
	if subType == '1':
		qry = '(1)'
	if subType == '2':
		qry = '(2)'
	if subType == '3':
		qry = '(3)'
	if subType == '4':
		qry = '(4)'
	aSQL = "SELECT ROUND(cast(sum(st_length(geom))as numeric) ,0) "
	aSQL = aSQL + "FROM " + sch + "." + spanTB + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND cn_feeder ='" + myFeed + "' "
	aSQL = aSQL + "AND subtype in " + qry
	aSQL = aSQL + "; "
	length = 0.0
	aCur.execute(aSQL)
	for row in aCur:
		aLength = row[0]
		if aLength is not None:
			length = aLength
	return(float(length))

#function for distro ring length	
def returnRingLength(mySub, myFeed, ring):
	if ring == '1':
		qry = '(1)'
	aSQL = "SELECT ROUND(cast(sum(st_length(geom))as numeric) ,0) "
	aSQL = aSQL + "FROM " + sch + "." + spanTB + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND cn_feeder ='" + myFeed + "' "
	aSQL = aSQL + "AND ring in " + qry
	aSQL = aSQL + "; "	
	# print (aSQL)
	# SELECT sum(st_length(geom)) 
	#	FROM data.span WHERE cn_substat = '19' 
	#	AND cn_feeder ='B224' 
	#	AND subtype in (1,2) ;
	length = 0.0
	aCur.execute(aSQL)
	for row in aCur:
		aLength = row[0]
		if aLength is not None:
			length = aLength
	return(float(length))






####################################
#########main


driveLoop()

aCur.close()
conn.close()
