#urban_analysis.py
#mike byrne
#makes metrics about availablilty in urban blocks

#updated by megan to support additional requirements
#	- count of structures along primary lines
#	- count of structures along underground/aerial



#variables and importing
import os
import psycopg2
import time
import json

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
sch = "singing_river" #"fcc" #"form_477_201712"

#tables
#input 
spanTB = "electric_span"
meterTB = "meter"
subTb = "substation"
structureTB = "structure"

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

	print ('sub_feeder,substation_name,substation#,feeder#,oh_primary_ft,oh_secondary_ft,ug_primary_ft,ug_secondary_ft,oh_primary_mi,oh_secondary_mi,ug_primary_mi,ug_secondary_mi,total_primary_miles,total_secondary_miles,meters,primary_poles,total_poles,ugtransformers')
	driveCur.execute(driveSQL)
	for driveRow in driveCur:
		aSub = driveRow[0]
		aFeed = driveRow[1]
		# print (aSub, aFeed)
		subName = returnSubName(aSub)
		# print (subName)
		aerial = returnSpanLength(aSub, aFeed, 'A')
		aerial2 = returnSpanLength(aSub, aFeed, 'A2')
		a_miles = round(aerial / 5280,2)
		a_miles2 = round(aerial2 / 5280,2)
		# print (aerial)
		ug = returnSpanLength(aSub, aFeed, 'U')
		ug2 = returnSpanLength(aSub, aFeed, 'U2')
		ug_miles = round(ug / 5280,2)
		ug_miles2 = round(ug2 / 5280,2)
		totMiles = round(a_miles + ug_miles ,2)
		totMiles2 = round(a_miles2 + ug_miles2,2)
		# print (ug)
		meters = returnMeters(aSub, aFeed)
		# print (meters)
		primPoles = returnPrimaryStructures(aSub, aFeed, 'primP')
		primTrans =returnPrimaryStructures (aSub, aFeed, 'primU')
		#print total primary poles and transformers
		totPoles = returnStructures(aSub, aFeed, 'p')
		ugtransformers = returnStructures(aSub, aFeed, 'u')
		#print(ugtrans)

		print (aSub + "-" + aFeed,subName,aSub,aFeed,aerial,aerial2,ug,ug2,a_miles,a_miles2,ug_miles,ug_miles2,totMiles,totMiles2,meters,primPoles,totPoles,ugtransformers)

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

#return the number of primary poles
def returnPrimaryStructures(mySub, myFeed, ugtrans):
	if ugtrans == 'primP':
		qry = "AND ugtrans = 0 "
		subQRY = "AND " + spanTB + "." + "subtype = 1 "
	if ugtrans == 'primU':
		qry = "AND ugtrans = 1 "
		subQRY = " "
	aSQL = "SELECT COUNT(distinct " + structureTB + ".gid) "
	aSQL = aSQL + "FROM " + sch + "." + structureTB + "," + sch + "." + spanTB + " "
	aSQL = aSQL + "WHERE " + structureTB + "." + "cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND " + structureTB + "." + "cn_feeder = '" + myFeed + "' "
	aSQL = aSQL + qry + " "
	aSQL = aSQL + "AND st_intersects(" + structureTB + "." + "geom" + "," + spanTB + "." + "geom" + ")" + " "
	aSQL = aSQL + subQRY
	aSQL = aSQL + "; "
	#SELECT COUNT(distinct structure.gid) 
	#FROM central_ok.structure, central_ok.electric_span
	#WHERE structure.cn_substat = '1' 
	#AND structure.cn_feeder = '1' 
	#AND structure.ugtrans = 0
	#AND st_intersects(structure.geom, electric_span.geom)
	#AND electric_span.subtype = 1
	count = 0
	aCur.execute(aSQL)
	for row in aCur:
		aCount = row[0]
		if aCount is not None:
			count = aCount
	return(count)


#return the number of structures:
def returnStructures(mySub, myFeed, ugtrans):
	if ugtrans == 'p':
		qry = '0'
	if ugtrans == 'u':
		qry = '1'
	aSQL = "SELECT COUNT(distinct gid) "
	aSQL = aSQL + "FROM " + sch + "." + structureTB + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND cn_feeder = '" + myFeed + "' "
	aSQL = aSQL + "AND ugtrans = " + qry
	aSQL = aSQL + "; "
	# print (aSQL) 
	# SELECT COUNT(distinct gid) 
	#	FROM data.poles 
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
	if subType == 'A':
		qry = '(1)'
	if subType == 'A2':
		qry = '(2)'
	if subType == 'U':
		qry = '(3)'
	if subType == 'U2':
		qry = '(4)'
	aSQL = "SELECT ROUND(cast(sum(st_length(geom))as numeric) ,0) "
	aSQL = aSQL + "FROM " + sch + "." + spanTB + " "
	aSQL = aSQL + "WHERE cn_substat = '" + mySub + "' "
	aSQL = aSQL + "AND cn_feeder ='" + myFeed + "' "
	aSQL = aSQL + "AND subtype in " + qry
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