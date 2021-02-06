import sys
import subprocess
import time
import os
import MySQLdb 
from Crypto.Util.number import long_to_bytes
import base64

sys.path.append('./modules')
from Utility import *
from Methods import *
from verify_encoding import *

def check_whitelist(word):
	x=open("./modules/whitelist.txt","r").read().strip().split('\n')
	for i in x:
		if i==word:
			return 1;
	return 0;

def check_whitelist_user_agent(word):
	x=open("./modules/whitelist_user_agent.txt","r").read().strip().split('\n')
	for i in x:
		if i==word:
			return 1;
	return 0;

def http_start():
	GETS=[]
	print("AM AJUNS AICI")
	ip=get_ip_address('ens33')  
	#ip='kali'
	start_http=1
	signatures=read_file('signatures')
	URLS=[]
	URL=''
	Cookie=''
	GET=[]
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	last_res=''
	while(start_http!=0):
		print ("------------------DADADADADADADA")
		added=0
		added_GET=0
		cmd="sudo tcpdump -i ens33 -A -s 0 'tcp dst port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'  -c 1 2>/dev/null"
		agent_found = 0
		cookie_found = 0
		host_found = 0
		get_found = 0
		founda = 0
		result = subprocess.check_output(cmd, shell=True).decode('utf-8')
		if "192.168.1.5" not in result:
			print ("REZULTAT NEALTERAT:",result)
			result=result.split("\n")
			print (result)
			for i in range(len(result)):
				result[i]=result[i].split(': ')
				if 'Agent' in result[i][0]:
					if agent_found == 0:
						if check_whitelist_user_agent(result[i][1]) == 0:
							agent_found = 1
							print ("User-Agent ALERT!")
							#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'User-Agent ALERT!','-','"+result[i][1]+"' )")
							cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'User-Agent!','MEDIUM','-','"+result[i][1]+"','"+str(datetime.now())+"')")
							db.commit()
							print ("USER AGENT GASIT!")
				if cookie_found == 0:
					if 'Cookie' in result[i][0]:
						Cookie=result[i][1]
						cookie_found = 1
				if host_found == 0:
					if 'Host' in result[i][0]:
						host_found = 1
						URL=result[i][1]
				if get_found == 0:
					if 'GET' in result[i][0]:
						GET=result[i][0]
						try:
							GET=GET.split('?')[1].split(' ')[0].split('&')
							for i in range(len(GET)):
								GET[i]=GET[i].split("=")
								get_found = 1
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
								get_found = 1
							else:
								GET=path
								get_found = 1
			stop=0
			banana=0
			for i in range(len(GETS)):
				if GETS[i] == GET[0][1:]:
					stop = 1
			print ("GETS:",GETS)
			print ("GET+++++",GET[0][1:])
			if banana == 0:
				GETS.append(GET[0][1:])
				auxiliar_URL=URL.split('.')
				new_URL=[]
				for i in range(len(auxiliar_URL)-1):
					if auxiliar_URL[i]!='www':
						new_URL.append(auxiliar_URL[i])
				print ("URL: ",'.'.join(new_URL))
				x=check_whitelist('.'.join(new_URL))
				if x == 0:
					if URL != '':
						if len(GET[0][1:]) > 0:
							print (verify_encoding(GET[0][1:]))
							if verify_encoding(GET[0][1:]) <= 10:
								if stop == 0:
									print ("ALERT! UNKNOWN BASE FOUND!!! --> "+ str(GET[0][1:]))
									#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'UNKNOWN BASE FOUND!!!','"+URL+"','"+GET[0][1:]+"' )")
									cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'ALERT! UNKNOWN BASE FOUND!','MEDIUM','"+URL+"','"+GET[0][1:]+"','"+str(datetime.now())+"')")
									db.commit()
									print ("AM AJUNS AICI!!!")
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
											if stop == 0:
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
											if stop == 0:
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
													if stop == 0:
														print ("ALERT! GET LEN: "+GET[count])
														#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET LENGTH!','"+URL+"','"+GET[count]+"' )")
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET LENGTH > 15','MEDIUM','"+URL+"','"+GET[count]+"','"+str(datetime.now())+"')")
														
														db.commit()
														break
												for count2 in range(len(signatures)):
													try:
														if founda==0:
															if long_to_bytes(signatures[count2] == base64.b64decode(GET[count])):
																if stop == 0:
																	print ("ALERT! GET FILE SIGNATURE FOUND AS BASE64! :"+GET[count])
																	#cursor.execute("INSERT INTO http (ID_event,Name,Alert_Type,Domain,Payload) VALUES('2', 'HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','"+URL+"','"+GET[count]+"' )")
																	cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', 'GET FILE SIGNATURE FOUND AS BASE64!','HIGH','"+URL+"','"+GET[count]+"','"+str(datetime.now())+"')")
																	db.commit()
																	founda=1
													except:
														pass
													if founda==0:
														if signatures[count2] == GET[count]:
															if stop == 0:
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




def stop_http():
	start_http=0
	
	
	
if len(sys.argv)>1:
	if sys.argv[1] == 'a':
		http_start()
