import sys
import subprocess
import time
from Crypto.Util.number import long_to_bytes
from urllib.parse import urlparse
import MySQLdb 
import re
import socket
import _thread

sys.path.append('./modules')
from Utility import *
from Methods import *
from verify_encoding import *
from VirusTotal import *
import rules

sys.path.append('./modules/MachineLearning')
import predict



def getPacketDetails():
	HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
	PORT = 9872        # Port to listen on (non-privileged ports are > 1023)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (HOST, PORT)
	sock.bind(server_address)
	sock.listen(1)

	while True:
		global continutPachetAPI
		global continutHexAPI
		global destinationAPI
		global sourceAPI
		global subdomainAPI
		ceva = [sourceAPI, destinationAPI, subdomainAPI, continutPachetAPI, continutHexAPI]
		connection, client_address = sock.accept()
		try:
			while True:
				connection.sendall('|'.join(ceva).encode())
				break;

		finally:
			connection.close()




global continutPachetAPI
continutPachetAPI = ''
global continutHexAPI
continutHexAPI = ''
global destinationAPI
destinationAPI = ''
global sourceAPI
sourceAPI = ''
global subdomainAPI
subdomainAPI = ''



def dns_start():
			_thread.start_new_thread(getPacketDetails,())
			dns_time=[]
			times=[]
			SUBD=[]
			puncte = 0
			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			configDetails = readConfig()
			ip=get_ip_address(configDetails['interface'])
			tld=read_file('TLD')
			signatures=read_file('signatures')
			database=[]
			global start_dns
			start_dns=1
			global continutPachetAPI
			global continutHexAPI
			global destinationAPI
			global sourceAPI
			global subdomainAPI
			while(start_dns!=0):
			#try:
				#cmd="-xxv -i "+configDetails['interface']+" -c1 -l -v -n -t port 53 2>/dev/null"
				ok_txt = 0
				puncte = 0
				#result = subprocess.check_output(cmd, shell=True).decode('utf-8')
				result = []
				nr_magic = 0
				last = 'a'
				last_last=''
				last_ML = 'a'
				last_last_ML =''
				p = subprocess.Popen(('sudo', 'tcpdump', '-l', '-xxv','port 53','-n','-v','-t'), stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
				for row in iter(p.stdout.readline, b''):
					if len(result) > 0:
						if row.strip().decode()[0] == 'I' and row.strip().decode()[1] == 'P':
							result = '\n'.join(result)
							for_check=result
							#print ("AICI E FORCHECK",for_check)
							HOST, continutHexAPI= rules.check_rules('DNS',for_check)
							continutPachetAPI = result.split('\n\t')[0]
							if (check_whitelist(HOST,"./modules/Filters/whitelist_sources.txt") == 0):
								sourceAPI = HOST
								result=result.split('\n\t')[0].replace('\t','')
							#try:
								result=result.split('\n')
								flag=result[0].split('[')[1].split(']')[0]
								for i in range(len(result)):
									res=result[i].split(' ')
									for j in range(len(res)):
										if res[j].replace('?','') == 'TXT':
											ok_txt = 1
										if res[j].count('.')>2:
											url=res[j].split('.')
										if res[j].count('.') == 2:
											puncte = 1
								#print ("FLAG:",flag)
								passed = 0
								if flag == 'none':
									try:
										for i in range(len(result)):
											scan_url=result[i].replace('\t','').split(' ')
											for j in range(len(scan_url)-1):
												if scan_url[j] == '>':
													url = scan_url[j+1]
										payload=result[1].split('?')[1].split(' ')[1]
										if 'addr' not in payload:
											if len(url[len(url)-2]) > 0:

												if payload.count('.') < 2:
													if len(payload)>0:
														raspuns_ML = predict.check_model_3(payload)
														if (raspuns_ML == 1):
															print ("SUBDOMENIU OK",payload)
														else:
															print ("SUBDOMENIU MALITIOS",payload)
															if payload != last_ML:
																cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('Machine Learning', 'DNS - DIG EXFILTRATION','HIGH','"+HOST+"','"+url[:-4]+"','"+payload+"','"+str(datetime.now())+"')")
																db.commit()
																last_last_ML = last_ML
																last_ML = payload
														subdomainAPI = payload
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DIG EXFILTRATION','HIGH','"+HOST+"','"+url[:-4]+"','"+payload+"','"+str(datetime.now())+"')")
														db.commit()
														passed = 1
												else:
													url = payload.split('.')

									
									except:
										pass
								try:
									url.remove("www")
								except:
									pass
								if passed == 0:
									nope=0
									if puncte == 0:
										if len(url)>4:
											nope = 1
									else:
										nope = 1


									for i in range(len(url)):
										if url[i]==None:
											del url[i]
									bd=url
									destinationAPI = '.'.join(url)
									exfil_check = 0
									exfil_check = check_TLD_exfil(bd,tld,HOST)
									if exfil_check == 0:
										domain=[]
										for i in range(len(tld)):
											tld[i]=tld[i].lower()
										for i in range(len(url)):
											for j in range(len(tld)):
												try:
													if url[i]==tld[j]:
														domain.append(url[i])
														del url[i]
													if url[i]=="www":
														del url[i]
														del bd[i]
												except:
													pass
										if ok_txt == 1:
											cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'TXT RECORDS','MEDIUM','"+HOST+"','"+bd[len(bd)-2]+"','-','"+str(datetime.now())+"')")
											db.commit()
										if (nope == 0) and (check_whitelist(bd[len(bd)-2],"./modules/Filters/whitelist.txt") == 0):
											z=DNS_time(bd[len(bd)-2],HOST)
											dns_ok=0
											if len(dns_time)>0:
												for k in range(len(dns_time)):
													if dns_time[k].domain == bd[len(bd)-2]:
														dns_ok = 1
														dns_time[k].add()
												if dns_ok == 0:
													dns_time.append(z)
											else:
												dns_time.append(z)

											var=check_whitelist(bd[len(bd)-2],"./modules/Filters/whitelist.txt")
											DNS_domain= "http://"+bd[len(bd)-2]+"."+'.'.join(domain)
											
											cursor3 = db.cursor()
											cursor3.execute("SELECT * FROM domains")
											data3 = (cursor3.fetchall())
											DNS_ok = 0
											for i in data3:
												if i[1] == DNS_domain:
													DNS_ok = 1
													break;
											if DNS_ok == 0:
												sql = "INSERT INTO domains (Domains) VALUES('"+DNS_domain+"')"
												cursor.execute(sql)
												db.commit()
											print ("AICI E DNSOK",DNS_ok)
											if var == 0:
												if DNS_ok == 0:
													#try:
														vt=search_url("http://"+bd[len(bd)-2]+"."+'.'.join(domain))
														for i in vt:
															cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('VirusTotal', '" + i[0] + "','HIGH','"+HOST+"','"+ bd[len(bd)-2] +"."+'.'.join(domain)+ "','" + i[2] + "','"+str(datetime.now())+"')")
															db.commit()
													#except:
														#print ("PASS BOSS")
														#pass
												stop = 0
												for i in range(len(SUBD)):
													if SUBD[i] == bd[0]:
														stop = 1
												if stop == 0:
													SUBD.append(bd[0])
													ok=0
													if len(bd)>2:
														for i in range(len(database)):
															if(database[i].check(bd[len(bd)-2])==1):
																for j in range(len(bd)-2):
																	subdomainAPI = bd[j]
																	if len(bd[j])>0:
																		raspuns_ML = predict.check_model_3(bd[j])
																		if (raspuns_ML == 1):
																			print ("SUBDOMENIU OK",bd[j])
																		else:
																			if bd[j] != last_ML:
																				print ("SUBDOMENIU MALITIOS",bd[j])
																				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('Machine Learning', 'DNS EXFILTRATION','UNKNOWN','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																				db.commit()
																				last_last_ML = last_ML
																				last_ML = bd[j]
																	

																	if len(str(bd[j])) > 10:
																		#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																		if bd[j] != last:	
																			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																			db.commit()
																			print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))) +" "+bd[j])
																			last_last = last
																			last = bd[j]
																		
																	if check_chars(bd[j]) == 1:
																		print ("ALERT! DNS EXFILTRATION NONASCII CHARS - " + bd[j])
																		#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																		if bd[j] != last:
																			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																			db.commit()
																			last_last = last
																			last = bd[j]
																	#print verify_encoding(bd[j])
																	if verify_encoding(bd[j])<=10:
																		print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
																		#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																		if bd[j] != last:
																			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																			db.commit()
																			last_last = last
																			last = bd[j]
																	kappa.add(bd[j],int(time.time()))
																ok=1

														if ok==0:
															#print ("Domain added! "+ bd[len(bd)-2])
															kappa=DNS(bd[len(bd)-2])
															for j in range(len(bd)-2):
																subdomainAPI = bd[j]
																kappa.add(bd[j],int(time.time()))
																if len(bd[j])>0:
																	raspuns_ML = predict.check_model_3(bd[j])
																	if (raspuns_ML == 1):
																		print ("SUBDOMENIU OK",bd[j])
																	else:
																		print ("SUBDOMENIU MALITIOS",bd[j])
																		if bd[j] != last_ML:
																			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('Machine Learning', 'DNS EXFILTRATION','UNKNOWN','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																			db.commit()
																			last_last_ML = last_ML
																			last_ML = bd[j]

																if len(str(bd[j])) > 10:
																	print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))))
																	if bd[j] != last:
																		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																		#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																		db.commit()
																		last_last = last
																		last = bd[j]
																if check_chars(bd[j]) == 1:
																	print ("ALERT! DNS EXFILTRATION NONASCII CHARS" + bd[j])
																	#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																	if bd[j] != last:
																		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																		db.commit()
																		last_last = last
																		last = bd[j]
																print ("AICI E ENCODING-ul:",verify_encoding(bd[j]))
																if verify_encoding(bd[j])<=10:
																	print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
																	#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
																	if bd[j] != last:
																		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																		db.commit()
																		last_last = last
																		last = bd[j]
															database.append(kappa)
													ok_signature = 0
													print ("AICI E OK_SIGNATURE:",ok_signature)
													for i in range(len(database)):
														if ok_signature == 0:
														#print (database[i].d,database[i].sd)
															for j in range(len(database[i].sd)):
																try:
																	for k in signatures:
																		if ok_signature == 0:
																			if k in database[i].sd[j]:
																				if ok_signature == 0:
																					print ("ALERT! DNS EXFILTRATION - " + str(k))
																					if bd[j] != last:
																						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'SIGNATURE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																						db.commit()
																						db.close()
																						last_last = last
																						last = bd[j]
																					ok_signature = 1
																except:
																	pass
										else:
											match = re.findall(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', '.'.join(url)) #match url
											if len(match) == 0:
												if( check_whitelist(bd[len(bd)-2],"./modules/Filters/whitelist.txt") == 0):
													raspuns_ML = predict.check_model_3('.'.join(url[:-2]))
													if len('.'.join(url[:-2]))>0:
														if (raspuns_ML == 1):
															print ("SUBDOMENIU OK",'.'.join(url[:-2]))
														else:
															print ("SUBDOMENIU MALITIOS",'.'.join(url[:-2]))
															if '.'.join(url[:-2]) != last_ML:
																cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('Machine Learning', 'DNS EXFILTRATION','UNKNOWN','"+HOST+"','"+''.join(bd[len(bd)-2])+"','"+'.'.join(url[:-2])+"','"+str(datetime.now())+"')")
																db.commit()
																last_last_ML = last_ML
																last_ML = '.'.join(url[:-2])
															ok_signature = 1

													z=DNS_time(bd[len(bd)-2],HOST)
													dns_ok=0
													if len(dns_time)>0:
														for k in range(len(dns_time)):
															if dns_time[k].domain == bd[len(bd)-2]:
																dns_ok = 1
																dns_time[k].add()
														if dns_ok == 0:
															dns_time.append(z)
													else:
														dns_time.append(z)
													
													for i in range(len(url)):
														tld_ver=0
														if url[i] not in tld:
															subdomainAPI = ''.join(bd[len(bd)-2])
															if verify_encoding(url[i]) != None:
																if verify_encoding(url[i]) <= 10:
																	if url[i] != last:
																		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+HOST+"','"+''.join(bd[len(bd)-2])+"','"+url[i]+"','"+str(datetime.now())+"')")
																		db.commit()	
																		last_last = last
																		last = url[i]
																		ok_signature = 1
							result = []
							nr_magic = 0
						if nr_magic > 2:
							nr_magic+=1
							result.append('\t'+row.strip().decode())
						else:
							nr_magic+=1
							result.append('    '+row.strip().decode())
					else:
						result.append(row.strip().decode())


			#except:
				#print ("PACHET MALFORMAT - DNS",result)
				#pass

def stop_dns():
	global start_dns
	start_dns=0

