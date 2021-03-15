from vt import *
import json
import time
import MySQLdb 
from datetime import datetime


def init():
	vt = VT()
	vt.setkey('03b3cc1de70a217d05e42394628e25971dbff611301f5efdb1c5188523f3bd66')
	return vt

def search_url(URL):
	for_return=[]
	vt=init()
	#print (vt.geturl("https://posta-romania.com/"))
	try:
		response=vt.geturl(URL)
		response=response['scans']
		for i,j in response.items():
			aux=[]
			if j['detected'] == True:
				aux.append(i)
				aux.append(j['detected'])
				aux.append(j['result'])
				for_return.append(aux)
	except:
		for_return=[]
		pass
	return for_return



def search_sha(URLs,nimic):
	time.sleep(25)
	for URL in URLs.split("|"):
		print ("INCA UNUL! @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		for_return=[]
		vt=init()
		#print (vt.geturl("https://posta-romania.com/"))
		try:
			response=vt.getfile(URL)
			response=response['scans']
			for i,j in response.items():
				aux=[]
				if j['detected'] == True:
					aux.append(i)
					aux.append(j['detected'])
					aux.append(j['result'])
					for_return.append(aux)
		except:
			for_return=[]
			pass
		print (for_return)
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta")
		cursor = db.cursor()
		for i in for_return:
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('VirusTotal', '" + i[0] + "','HIGH','"+"Android"+"','"+ URL + "','" + i[2] + "','"+str(datetime.now())+"')")
			db.commit()
		db.close()