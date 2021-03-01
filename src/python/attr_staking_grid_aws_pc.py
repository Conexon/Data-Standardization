
#attr_staking_grid.py - attributes the staking grid

#mike byrne/luisa 
#july 26, 2018

#create the fiber cable model (version 0.1)

#variables and importing
#variables and importing
import os
import psycopg2
import time
import json

#DB
myDB = "standardize" # "tn_grant" #fcc

#connection
conFile = './connection.json'
with open (conFile) as data_connection:
	var_connection = json.load(data_connection) 
myHost = var_connection["myHost"] #
myPort = var_connection["myPort"] #
myUser = var_connection["myUser"] #
myPWord = var_connection["myPWord"] #

myConn = "dbname=" + myDB + " host=" + myHost + " port=" + myPort + " user=" + myUser + " password=" + myPWord
FNULL = open(os.devnull, 'w')

#schema/prefix/workorder/projection
sch = "singing_river" #"fcc" #"form_477_201712"

db = "standardize"
sch = "singing_river"

#tables
stTB = "stakinggrid3000"
conTB = "electric_span"

#fields - staking grid
stTBID = "gid"
stTBGeo = "geom"
stSubCd = "subcode"

#fields - span
conTBID = "gid"
conTBGeo = "geom"
conSub = "cn_substat"
conFeed = "cn_feeder"


#
#******************************************************
#						FUNCTIONS
#******************************************************
#
#driver - loop for every gid in the staking grid table
#do these things
#	- return a list of substation / feeders that that page overlaps
#	- populate a staking grid field with that list
def drive():
	driveCur = conn.cursor()
	dSQL = "SELECT gid "
	dSQL = dSQL + "FROM " + sch + "." + stTB + " "
	#dSQL = dSQL + "WHERE gid in  (988,4446,4249,9838,9661) "
	# dSQL = dSQL + "WHERE gid in  (4446) "
	# dSQL = dSQL + "WHERE gid in (10412, 11310) "
	dSQL = dSQL + "ORDER BY gid "
	#dSQL = dSQL + "LIMIT 10" ###doing this just for debugging purposes
	dSQL = dSQL + "; "
	print (dSQL)
	#SELECT gid FROM data.stakinggrid3000 
	#	ORDER BY gid 
	#	LIMIT 1;

	driveCur.execute(dSQL)
	for row in driveCur:
		myPG = str(row[0])
		print (myPG)
		myStr = retSubFeeders(myPG)
		print (myStr)
		updGrid(myPG, myStr)
	driveCur.close()

#this function updates the staking grid with the new string
def updGrid(myID, SubFeedStr):
	updSQL = "UPDATE " + sch + "." + stTB + " "
	updSQL = updSQL + "SET " + stSubCd + "='"
	updSQL = updSQL + SubFeedStr + "' "
	updSQL = updSQL + "WHERE " + stTBID + "=" + myID
	updSQL = updSQL + "; "
	updSQL = updSQL + "COMMIT; "
	print (updSQL)
	#UPDATE data.stakinggrid3000 SET cn_subcode='DV_344, IM_324' WHERE gid=4446; 
	theCur.execute(updSQL)


#return the substation / feeder that that page overlaps
def retSubFeeders(aPG):
	myList = []
	myStr = ""
	mySQL = "SELECT " + conTB + "." + conSub + "," + conTB + "." + conFeed + ", count(*) "
	mySQL = mySQL + "FROM " + sch + "." + conTB + "," + sch + "." + stTB + " "
	mySQL = mySQL + "WHERE ST_Intersects(" + conTB + "." + conTBGeo + "," + stTB + "." + stTBGeo + ") "
	mySQL = mySQL + "AND " + stTB + "." + stTBID + "=" + aPG + " "
	mySQL = mySQL + "GROUP BY " + conTB + "." + conSub + "," + conTB + "." + conFeed + " "
	mySQL = mySQL + "ORDER BY " + conTB + "." + conSub + "," + conTB + "." + conFeed + " "
	mySQL = mySQL + "; "
	# print mySQL
	#SELECT consumers.ml_substat,consumers.ml_feeder, count(*) 
	#	FROM data.consumers,data.stakinggrid3000 
	#	WHERE ST_Intersects(consumers.geom,stakinggrid3000.geom) 
	#	AND stakinggrid3000.gid=4446 
	#	GROUP BY consumers.ml_substat,consumers.ml_feeder 
	#	ORDER BY consumers.ml_substat,consumers.ml_feeder ; 
	theCur.execute(mySQL)
	for row in theCur:
		myList.append(str(row[0]) + "_" + str(row[1]))
		# print myList

	myStr = ', '.join(myList)
	return(myStr)

#
#******************************************************
#						MAIN 
#******************************************************
#	

myConn = "dbname=" + myDB + " host=" + myHost + " port=" + myPort + " user=" + myUser + " password=" + myPWord
conn = psycopg2.connect(myConn)
theCur = conn.cursor()


drive()


theCur.close()

#end
print ("		finished")
now = time.localtime(time.time())
print ("end time:", time.asctime(now))