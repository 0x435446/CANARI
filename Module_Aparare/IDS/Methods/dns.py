import sys
import subprocess
import time
sys.path.append('../')
from Utility import *
from Methods import *
from verify_encoding import *
from Crypto.Util.number import long_to_bytes
from urllib.parse import urlparse
import MySQLdb 

def check_chars(word):
	for i in range(len(word)):
		if ord(word[i])<=0x20 or ord(word[i]) >=ord('z'):
			return 1
	return 0


times=[]

db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
cursor = db.cursor()


ip=get_ip_address('ens33')  
tld=read_file('TLD')
signatures=read_file('signatures')

database=[]


while(1):
	cmd="tcpdump -i ens33 -c1 -l -v -n -t port 53"
	result = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\t','').split('\n')
	print (result)
	res = []
	flag=result[0].split('[')[1].split(']')[0]
	result[0]=result[1].split()
	for val in result[0]: 
		if val != None : 
			res.append(val) 
	index_value=0
	for i in range(len(res)):
		if "." in res[i] and ":" not in res[i]:
			index_value=i
	print (res[index_value])
	url=res[index_value].split('.')
	for i in range(len(url)):
		if url[i]==None:
			del url[i]
	bd=url
	for i in range(len(tld)):
		tld[i]=tld[i].lower()
	for i in range(len(url)):
		for j in range(len(tld)):
			try:
				if url[i]==tld[j]:
					del url[i]
				if url[i]=="www":
					del url[i]
					del bd[i]
			except:
				pass
	print ("AICI e domeniul: ",bd[len(bd)-2])
	ok=0
	if flag == 'none':
		if len(bd[len(bd)-2])>0:
			print ("DIG EXFILTRATION",bd[len(bd)-2],"catre",res[2][:-4])
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'DIG EXFILTRATION','HIGH','"+ res[2][:-4]+"','"+bd[len(bd)-2]+"','"+str(datetime.now())+"')")
	if len(bd)>2:
		for i in range(len(database)):
			if(database[i].check(bd[len(bd)-2])==1):
				for j in range(len(bd)-2):
					if len(str(bd[j])) > 10:
						#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
						db.commit()
						print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))) +" "+bd[j])
						
					if check_chars(bd[j]) == 0:
						print ("ALERT! DNS EXFILTRATION NONASCII CHARS - " + bd[j])
						#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
						db.commit()
					#print verify_encoding(bd[j])
					if verify_encoding(bd[j])<=10:
						print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
						#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
						db.commit()
					kappa.add(bd[j],int(time.time()))
				ok=1

		if ok==0:
			print ("Domain added! "+ bd[len(bd)-2])
			kappa=DNS(bd[len(bd)-2])
			for j in range(len(bd)-2):
				kappa.add(bd[j],int(time.time()))
				if len(str(bd[j])) > 10:
					print ("ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j]))))
					cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION LENGTH','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
					#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION LENGTH','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
					db.commit()
				if check_chars(bd[j]) == 1:
					print ("ALERT! DNS EXFILTRATION NONASCII CHARS" + bd[j])
					#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'DNS EXFILTRATION NONASCII CHARS','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
					cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'DNS EXFILTRATION NONASCII CHARS','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
					db.commit()
				if verify_encoding(bd[j])<=10:
					print ("ALERT! UNKNOWN BASE FOUND!!! --> "+bd[j])
					#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'UNKNOWN BASE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
					cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'UNKNOWN BASE FOUND','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
					db.commit()
			database.append(kappa)

	for i in range(len(database)):
		print (database[i].d,database[i].sd)
		for j in range(len(database[i].sd)):
			try:
				for k in signatures:
					if k in database[i].sd[j]:
						print ("ALERT! DNS EXFILTRATION - " + str(k))
						#cursor.execute("INSERT INTO dns (ID_event,Name,Alert_Type,Domain,Subdomain) VALUES('1', 'DNS', 'SIGNATURE FOUND','"+bd[len(bd)-2]+"','"+bd[j]+"' )")
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'SIGNATURE FOUND','HIGH','"+bd[len(bd)-2]+"','"+bd[j]+"','"+str(datetime.now())+"')")
						db.commit()
			except:
				pass


