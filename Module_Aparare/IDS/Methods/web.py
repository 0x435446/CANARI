import sys
import subprocess
import time
import os
sys.path.append('../')
from Utility import *
from Methods import *
from Crypto.Util.number import long_to_bytes
import base64
from verify_encoding import *
import MySQLdb 

ip=get_ip_address('ens33')  
#ip='kali'


signatures=read_file('signatures')
URLS=[]
URL=''
Cookie=''
GET=[]
db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
cursor = db.cursor()
while(1):
	added=0
	added_GET=0
	cmd="tcpdump -A -s 0 'tcp dst port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'  -c 1"
	founda=0
	result = subprocess.check_output(cmd, shell=True).decode('utf-8').split("\n")
	print (result)
	for i in range(len(result)):
		result[i]=result[i].split(': ')
		if 'Agent' in result[i][0]:
			if result[i][1] != 'Chosen Agent':
				print ("User-Agent ALERT!")
				#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'User-Agent ALERT!','-','"+result[i][1]+"' )")
				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'User-Agent!','MEDIUM','-','"+result[i][1]+"','"+str(datetime.now())+"')")

				db.commit()
		if 'Cookie' in result[i][0]:
			Cookie=result[i][1]
		if 'Host' in result[i][0]:
			URL=result[i][1]
		if 'GET' in result[i][0]:
			GET=result[i][0]
			try:
				GET=GET.split('?')[1].split(' ')[0].split('&')
				for i in range(len(GET)):
					GET[i]=GET[i].split("=")
			except:
				GET=GET.split(' ')
				path=[]
				path2=[]
				for counter in range(len(GET)):
					if "HTTP" in GET[counter]:
						path.append(GET[counter-1])
						path2.append(GET[counter])
				if "GET" in str(path):
					GET=path2
				else:
					GET=path
	print (GET)
	if URL!='':
		if len(GET[0][1:])>0:
			print (verify_encoding(GET[0][1:]))
			if verify_encoding(GET[0][0:])<=10:
				print ("ALERT! UNKNOWN BASE FOUND!!! --> "+ str(GET[0][1:]))
				#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'UNKNOWN BASE FOUND!!!','"+URL+"','"+GET[0][1:]+"' )")
				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'ALERT! UNKNOWN BASE FOUND!','MEDIUM','"+URL+"','"+GET[0][1:]+"','"+str(datetime.now())+"')")
				db.commit()
		if len(URLS) == 0:
			x=WEB()
			try:
				x.add(URL,Cookie,GET,str(int(time.time())))
			except:
				x.add(URL,Cookie,[],str(int(time.time())))
			for count2 in range(len(signatures)):
				try:
					if founda==0:
						if long_to_bytes(signatures[count2] == base64.b64decode(GET[0])):
							print ("ALERT! GET FILE SIGNATURE FOUND AS BASE64! :"+GET[0])
							#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','"+URL+"','"+GET[0]+"' )")
							cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','HIGH','"+URL+"','"+GET[0]+"','"+str(datetime.now())+"')")

							db.commit()
							founda=1
				except:
					pass
				try:
					if founda==0:
						if signatures[count2] in GET[0]:
							print ("ALERT! GET FILE SIGNATURE FOUND AS HEX! :"+GET[0])
							#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET FILE SIGNATURE FOUND AS HEX!','"+URL+"','"+GET[0]+"' )")
							cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET FILE SIGNATURE FOUND AS HEX!','HIGH','"+URL+"','"+GET[0]+"','"+str(datetime.now())+"')")
							
							db.commit()
							founda=1
				except:
					pass
			URLS.append(x)
		else:
			ok=0
			for i in range(len(URLS)):
					if URL==URLS[i].URL:
						for ii in range(len(URLS[i].GET)):
							ok3=0
							if URLS[i].GET[ii] == GET:
								ok3=1
						if ok3== 0:
							URLS[i].GET.append(GET)
							URLS[i].GET_time.append(str(int(time.time())))
							for count in range(len(GET)):
								if len(GET[count])>15:
									print ("ALERT! GET LEN: "+GET[count])
									#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET LENGTH!','"+URL+"','"+GET[count]+"' )")
									cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET LENGTH > 15','MEDIUM','"+URL+"','"+GET[count]+"','"+str(datetime.now())+"')")
									
									db.commit()
									break
								for count2 in range(len(signatures)):
									try:
										if founda==0:
											if long_to_bytes(signatures[count2] == base64.b64decode(GET[count])):
												print ("ALERT! GET FILE SIGNATURE FOUND AS BASE64! :"+GET[count])
												#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','"+URL+"','"+GET[count]+"' )")
												cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','HIGH','"+URL+"','"+GET[count]+"','"+str(datetime.now())+"')")
												db.commit()
												founda=1
									except:
										pass
									if founda==0:
										if signatures[count2] == GET[count]:
											print ("ALERT! GET FILE SIGNATURE FOUND AS HEX! :"+GET[count])
											#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET FILE SIGNATURE FOUND AS HEX!','"+URL+"','"+GET[count]+"' )")
											cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET FILE SIGNATURE FOUND AS HEX!','HIGH','"+URL+"','"+GET[count]+"','"+str(datetime.now())+"')")											
											db.commit()
											founda=1
						print ("AM AJUNS LA COOKIES")
						print (URLS[i].adds)
						for ii in range(len(URLS[i].Cookies)):
							ok2=0
							if URLS[i].Cookies[ii] == Cookie:
								ok2=1
						if ok2 == 0:
							URLS[i].Cookies.append(Cookie)
							URLS[i].adds+=1
							if URLS[i].adds>2:
								print ("ALERT! MULTIPLE COOKIES SENT TO "+ URLS[i].URL)
								#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'MULTIPLE COOKIES SENT','"+URL+"','"+URLS[i].URL+"' )")
								cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'MULTIPLE COOKIES SENT','HIGH','"+URLS[i].URL+"','"+Cookie+"','"+str(datetime.now())+"')")											
								db.commit()
						ok=1

			if ok==0:
				x=WEB()
				try:	
					x.add(URL,Cookie,GET,str(int(time.time())))
				except:
					x.add(URL,Cookie,[],str(int(time.time())))
				URLS.append(x)

	for i in range(len(URLS)):
		print (URLS[i].URL,str(URLS[i].Cookies),str(URLS[i].GET),str(URLS[i].GET_time))





