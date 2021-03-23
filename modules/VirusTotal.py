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



def search_sha(URLs,adresa):
	print ("ADRESAA:",adresa)
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta")
	cursor2= db.cursor()
	cursor2.execute("SELECT * FROM applications")
	data2 = (cursor2.fetchall())
	for_print=[]
	for URL in URLs.split("|"):
		time.sleep(25)
		for_return=[]
		vt=init()
		#print (vt.geturl("https://posta-romania.com/"))
		to_json=''
		ok = 0
		for i in data2:
			if i[1] == URL :
				ok +=1
				if i[2] == adresa:
					ok +=1
					break;
		if ok < 2:
			try:
				response=vt.getfile(URL)
				for_print.append(response)
				to_json=response
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
				print ("NU AM AJUNS UNDE TREBUIE!")
				pass
			#print (for_return)
			#for_insert=MySQLdb.escape_string(str(for_return))
			#cursor2.execute("INSERT INTO applications (SHA,IP) VALUES('"+URL+"','"+adresa+"')")
			#cursor2.execute("INSERT INTO applications (SHA,IP,JSON) VALUES('"+URL+"','"+adresa+"','"+str(for_insert)+"')")
			escaped  = MySQLdb.escape_string(str(to_json))
			#print ("AICI E escaped", escaped)
			sql = "INSERT INTO applications (SHA,IP,JSON) VALUES('"+URL+"','"+adresa+"','"+escaped.decode()+"')"
			cursor2.execute(sql)
			db.commit()
			print ("INCA UNUL! @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   ",URL)
			cursor = db.cursor()
			for i in for_return:
				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('VirusTotal', '" + i[0] + "','HIGH','"+"Android"+"','"+ URL + "','" + i[2] + "','"+str(datetime.now())+"')")
				db.commit()
	db.close()