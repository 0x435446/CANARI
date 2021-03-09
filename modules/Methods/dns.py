import sys
import subprocess
import time
from Crypto.Util.number import long_to_bytes
from urllib.parse import urlparse
import MySQLdb 
import re
sys.path.append('./modules')
from Utility import *
from Methods import *
from verify_encoding import *
from VirusTotal import *
import rules

def check_chars(word):
	for i in range(len(word)):
		if ord(word[i])<=0x20 or ord(word[i]) >=ord('z'):
			if ord(word[i])!=0xa or ord(word[i])!=0xd:
				return 1
	return 0


def check_whitelist(word,path):
	x=open(path,"r").read().strip().split('\n')
	if path == "./modules/whitelist_sources.txt":
		for i in x:
			if i in word:
				return 1
	else:
		for i in x:
			if i in word.split('.'):
				return 1;
	return 0;


def check_TLD_exfil(URL,tld,HOST):
	nr = 0
	DESTIONATION = []
	for i in URL:
		if i.upper() in tld or i.lower() in tld:
			nr+=1
		else:
			DESTIONATION.append(i)
	if nr > 3:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
		cursor = db.cursor()
		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'TLD EXFILTRATION','HIGH','"+HOST+"','"+'.'.join(DESTIONATION)+"','"+'.'.join(URL)+"','"+str(datetime.now())+"')")
		db.commit()
		db.close()
		return 1
	return 0


def dns_start():
	dns_time=[]
	times=[]
	SUBD=[]
	puncte = 0
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	ip=get_ip_address('ens33')  
	tld=read_file('TLD')
	signatures=read_file('signatures')
	database=[]
	global start_dns
	start_dns=1
	while(start_dns!=0):
		cmd="sudo tcpdump -xxv -i ens33 -c1 -l -v -n -t port 53 2>/dev/null"
		ok_txt = 0
		puncte = 0
		result = subprocess.check_output(cmd, shell=True).decode('utf-8')
		for_check=result
		HOST = rules.check_rules('DNS',for_check)
		if check_whitelist(HOST,"./modules/whitelist_sources.txt") == 0:
			result=result.split('\n\t')[0].replace('\t','')
			try:
				if '192.168.1.4' not in result:
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
							print ("AICI E URL",url)
							if 'addr' not in payload:
								if len(url[len(url)-2]) > 0:
									if payload.count('.') < 2:
										cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DIG EXFILTRATION','HIGH','"+HOST+"','"+url[:-4]+"','"+payload+"','"+str(datetime.now())+"')")
										db.commit()
										passed = 1
									else:
										print ("PASSED")
										url = payload.split('.')
						except:
							pass
					for i in range(len(url)):
						if url[i]=="www":
							del url[i]
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
							if nope == 0 :
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
								
								var=check_whitelist(bd[len(bd)-2],"./modules/whitelist.txt")
								if var == 0:
									try:
										vt=search_url("http://"+bd[len(bd)-2]+"."+'.'.join(domain))
										#print (vt)
										for i in vt:
											cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('VirusTotal', '" + i[0] + "','HIGH','"+HOST+"','"+ bd[len(bd)-2] +"."+'.'.join(domain)+ "','" + i[2] + "','"+str(datetime.now())+"')")
											db.commit()
									except:
										pass
									print ("AICI E URL DE LA DNS!",domain)
									stop = 0
									#print ("SUBDOMENII:",SUBD)
									for i in range(len(SUBD)):
										if SUBD[i] == bd[0]:
											stop = 1
									#print ("AICI SUNT ASTEA:",SUBD)
									if stop == 0:
										SUBD.append(bd[0])
										ok=0
										if len(bd)>2:
											for i in range(len(database)):
												if(database[i].check(bd[len(bd)-2])==1):
													for j in range(len(bd)-2):
														if len(str(bd[j])) > 10:
															#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
															cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
															db.commit()
															print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))) +" "+bd[j])
															
														if check_chars(bd[j]) == 1:
															print ("ALERT! DNS EXFILTRATION NONASCII CHARS - " + bd[j])
															#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
															cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
															db.commit()
														#print verify_encoding(bd[j])
														if verify_encoding(bd[j])<=10:
															print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
															#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
															cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
															db.commit()
														kappa.add(bd[j],int(time.time()))
													ok=1

											if ok==0:
												#print ("Domain added! "+ bd[len(bd)-2])
												kappa=DNS(bd[len(bd)-2])
												for j in range(len(bd)-2):
													kappa.add(bd[j],int(time.time()))
													if len(str(bd[j])) > 10:
														print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))))
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
														#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
														db.commit()
													if check_chars(bd[j]) == 1:
														print ("ALERT! DNS EXFILTRATION NONASCII CHARS" + bd[j])
														#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
														db.commit()
													if verify_encoding(bd[j])<=10:
														print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
														#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
														db.commit()
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
																		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'SIGNATURE FOUND','HIGH','"+HOST+"','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
																		db.commit()
																		db.close()
																		ok_signature = 1
													except:
														pass
							else:
								match = re.findall(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', '.'.join(url)) #match url
								if len(match) == 0:
									if( check_whitelist(bd[len(bd)-2],"./modules/whitelist.txt") == 0):
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
											if verify_encoding(url[i]) != None:
												if verify_encoding(url[i]) <= 10:
													if url[i] not in tld:
														cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND 2','HIGH,'"+HOST+"','"+''.join(bd[len(bd)-2])+"','"+url[i]+"','"+str(datetime.now())+"')")
														db.commit()
														print (verify_encoding(url[i]),url[i])
			except:
				print ("PACHET MALFORMAT - DNS",result)
				pass

def stop_dns():
	global start_dns
	start_dns=0

