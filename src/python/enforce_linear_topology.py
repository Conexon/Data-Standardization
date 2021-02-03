#enforce_linear_topology.py 
#	enforces the spatial linear model by ensuring all lines are split at nodes
#	some input span lines are often not split at nodes causing significant
#	topological errors later
#mike byrne
#jan 13, 2021

#workflow
#	- make sure all line segments are single geometry line segments
#	- then make sure all line segments are split at nodes
#	- for every linesegment, in order of length 
#		(theory being that the doing smaller lines before longer one will grab all lines that need to be split)
#		- acquire the id, the start point and the end point (as geomety)
#		- find what other than is connected to the start/end point
#		- for those lines see if, the point is along, or at the end of that line
#			- if the point is along the line (not at the end), then
#				- it needs to be split; and delete the original line
#	- there will be resulting duplicate lines; remove these at the end
#		- this has the added benefit of removing duplicate lines that could have been there
#		from the begining

#variables and importing
import psycopg2
import time
import json 
from datetime import datetime

startNow = datetime.now()
print ("start time:", startNow)

db = "in_scremc"
host = "localhost"
port = "5432"
user = "mike"
pWord = ""
#connection
myConn = "dbname=" + db + " host=" + host + \
	" port=" + port + " user=" + user + \
	" password=" + pWord

# print (myConn)
#schema/prefix/prj
sch = "data"	
# global pre
spanTB = "span"

#make database connection - so that we can use cursors to update the table
global conn
conn = psycopg2.connect(myConn)
conn.autocommit = True
driveCur = conn.cursor()
aCur = conn.cursor()
insCur = conn.cursor()		
delCur = conn.cursor()

#table names

#field global variables
#use span as the template for field names
gidFld = "gid" #var_tables_fields["span"]["gidFld"]#"gid"  
subFld = "cn_substat" #var_tables_fields["span"]["StandardSubstatFld"]#"cn_substat"
feedFld = "cn_feeder"  #var_tables_fields["span"]["StandardFeederFld"]#"cn_feeder"
subTypeFld = "subtype" #var_tables_fields["span"]["cnSubtype"]#"subtype"
geoFld = "geom "#ar_tables_fields["span"]["geoFld"]#"geom"

#
snapDist = '1' #"0.001"
#
#******************************************************
#						VARIABLES
#******************************************************
#
#drive for every line segment in the design run
#	we order by length here, b/c that way it starts looking for lines to split with the shortest lines
#	in theory this should result in taking care of all unspit lines assuming the lines that need to be split
#	are longer than others
def driveToSplit():
	driveSQL = "SELECT " + gidFld + ","
	driveSQL = driveSQL + "ST_StartPoint((ST_Dump(geom)).geom) as startGeom,"
	driveSQL = driveSQL + "ST_EndPoint((ST_Dump(geom)).geom) as endGeom "
	driveSQL = driveSQL + "FROM " + sch + "." + spanTB + " "
	driveSQL = driveSQL + "ORDER BY ST_Length(geom) "
	driveSQL = driveSQL + "; "
	# print (driveSQL)
	# SELECT gid,
	# 		ST_StartPoint((ST_Dump(geom)).geom) as startGeom,
	# 		ST_EndPoint((ST_Dump(geom)).geom) as endGeom 
	# 	FROM data.span 
	# 	ORDER BY ST_Length(geom) 
	# ; 

	splitList = []
	driveCur.execute(driveSQL, [])
	for driveRow in driveCur:
		#for each endpoint, 
		inLineGID = driveRow[0]
		# print (inLineGID)
		for aPoint in [driveRow[1], driveRow[2]]:
			#returns a list of lists with this structure
			#	[0:id of connecting line; 1:geometry of connecting line]
			conLinesList = retConnectingLine(inLineGID, aPoint)
			# print (conLinesList)
			for conLine in conLinesList:
				needToSplit = doesLineNeedToBeSplit(conLine,aPoint)
				if needToSplit == 1:
					# print( "connecting line: ", conLine[0], needToSplit)
					#then split this line at that point
					splitLine(conLine, aPoint)
					deleteOriginalLine(conLine[0])
					if conLine[0] not in splitList:
						splitList.append(conLine[0])
	# print (splitList)
	print (len(splitList))
					
#see if we need to split this line
def doesLineNeedToBeSplit(conLineList, aPointGeom):
	needToSplit = 0
	mySQL = "SELECT ST_LineLocatePoint(%s,%s) "
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT ST_LineLocatePoint(%s,%s) ;
	aCur.execute(mySQL, [conLineList[1], aPointGeom])
	for row in aCur:
		# print(row[0])
		if row[0] > 0 and row[0] < 1:
			needToSplit = 1

	return(needToSplit)

#return connecting lines of the point entered
def retConnectingLine(aInLineID, aPointGeom):
	myList = []
	mySQL = "SELECT " + gidFld + ",(ST_Dump(" + geoFld + ")).geom as geom "
	mySQL = mySQL + "FROM " + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE ST_DWithin(" + spanTB + "." + geoFld + ","
	mySQL = mySQL + "%s, 1) "
	mySQL = mySQL + "AND " + gidFld + "!= %s "
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT gid,(ST_Dump(geom)).geom as geom 
	# 	FROM design.s1_f3_span 
	# 	WHERE ST_DWithin(s1_f3_span.geom,%s, 1) 
	# 	AND gid!= %s 
	# 	; 
	aCur.execute(mySQL, [aPointGeom, aInLineID])
	for row in aCur:
		myList.append([ row[0], row[1] ])
	return(myList)

#delete the original gid
def deleteOriginalLine(aGID):
	# print (aGID)
	mySQL = "DELETE FROM " + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE " + gidFld + "=%s "
	mySQL = mySQL + "; COMMIT; "
	# print (mySQL)
	# DELETE 
	# 	FROM data.span 
	# 	WHERE gid=%s 
	# 	; COMMIT;  
	delCur.execute(mySQL, [aGID])

#insert a new row for each geometry array in this gid row
def splitLine(conLineList, aPointGeom):  #(conLine, aPoint)
	mySQL = "SELECT (ST_Dump(ST_Split(ST_Snap(%s,%s," + snapDist + "),%s))).geom " 
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT (ST_Dump(ST_Split(ST_Snap(%s,%s,1),%s))).geom 
	# 	;
	aCur.execute(mySQL,[ conLineList[1], aPointGeom, aPointGeom ])
	for newLineRow in aCur:
		insSQL = "INSERT INTO " + sch + "." + spanTB + " "
		# insSQL = "INSERT INTO data.working " - for testing
		insSQL = insSQL + "(" + geoFld + "," + subFld + "," + feedFld + "," + subTypeFld + ") "  
		insSQL = insSQL + "SELECT ST_Multi(%s), "
		insSQL = insSQL + subFld + "," + feedFld + "," + subTypeFld + " " 
		insSQL = insSQL + "FROM " + sch + "." + spanTB + " "
		insSQL = insSQL + "WHERE " + gidFld + "=%s "
		insSQL = insSQL + "; COMMIT; "
		# print (insSQL)
		# INSERT INTO data.span 
		#	(geom,cn_substat,cn_feeder,subtype,ring,ring_size,guid) 
		# 	SELECT ST_Multi(%s), cn_substat,cn_feeder,subtype,ring,ring_size,uuid_generate_v1() 
		# 	FROM data.span WHERE gid=%s 
		# 	; COMMIT; 
		insCur.execute(insSQL, [ newLineRow[0], conLineList[0] ]) 

#delete duplicate lines
def delDuplicateLines():
	mySQL = "DELETE FROM "
	mySQL = mySQL + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE " + gidFld + " IN " 
	mySQL = mySQL + "( "
	mySQL = mySQL + "SELECT b." + gidFld + " "
	mySQL = mySQL + "FROM " + sch + "." + spanTB + " a, " + sch + "." + spanTB + " b "
	mySQL = mySQL + "WHERE st_equals(a.geom, b.geom) "
	mySQL = mySQL + "AND a." + gidFld + "<b." + gidFld + " "
	mySQL = mySQL + ") "
	mySQL = mySQL + "; COMMIT; "
	# print (mySQL)
	# DELETE FROM 
	# data.span
	# WHERE gid in 
	# (
	# 	SELECT b.gid
	# 		FROM data.span a, data.span b
	#  		WHERE a.gid < b.gid
	#  		AND ST_EQUALS(a.geom, b.geom)
  	# )
	# ;
	delCur.execute(mySQL, [])
	
	return()

#enforce single Lines
#while all lines are defined in our DB as `MultiLineString`
#	there should be only 1 geometry per row
#	this function ensures that
#	if row has > 1 geometry, explode all of those geometries
def singleLine():
	mySQL = "SELECT " + gidFld + ", ST_NumGeometries(" + geoFld + ") "
	mySQL = mySQL + "FROM " + sch + "." + spanTB + " "
	mySQL = mySQL + "WHERE ST_NumGeometries(" + geoFld + ") >1 "	
	mySQL = mySQL + "ORDER BY " + gidFld + " "
	mySQL = mySQL + "; "
	# print (mySQL)
	# SELECT gid, ST_NumGeometries(geom) 
	#	FROM data.span 
	#	WHERE ST_NumGeometries(geom) >1 
	#	ORDER BY gid 
	#	; 
	aCur.execute(mySQL)
	# print (aCur.rowcount)
	if aCur.rowcount > 0:
		#get subtype value for that line
		#explode that line
		#remove the original line
		for row in aCur:
			myGID = row[0]
			# print (myGID)
			insertNewRows(spanTB, myGID)
			deleteOriginalLine(myGID)
	return()

#insert a new row for each geometry array in this gid row
def insertNewRows(aTB, aGID):
	insSQL = "INSERT INTO " + sch + "." + aTB + " "
	insSQL = insSQL + "(geom, cn_substat, cn_feeder, subtype) "
	insSQL = insSQL + "SELECT ST_Multi((ST_Dump(geom)).geom), cn_substat, cn_feeder, subtype "
	insSQL = insSQL + "FROM " + sch + "." + aTB + " "
	insSQL = insSQL + "WHERE " + gidFld + "= %s  "
	insSQL = insSQL + "; COMMIT; "
	# print (insSQL)
	# INSERT INTO data.span 
	#	(geom, cn_substat, cn_feeder, subtype, ring, ring_size) 
	#	SELECT ST_Multi((ST_Dump(geom)).geom), %s, %s, subtype, ring, ring_size 
	#	FROM data.span WHERE gid= %s  
	# 	; 
	# COMMIT;
	insCur.execute(insSQL,[aGID])


#
#******************************************************
#						MAIN 
#******************************************************
#	

singleLine()
driveToSplit()
delDuplicateLines()

#clean up
driveCur.close()
aCur.close()
insCur.close()
delCur.close()
conn.close()

print ("		finished " )
endNow = datetime.now()
# return()
print ("end time:", endNow)
diff = endNow - startNow
print (diff)
#end
