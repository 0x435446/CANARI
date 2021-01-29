import sys
import subprocess
sys.path.append('../')
from Utility import *
from Methods import *
import MySQLdb 
from datetime import datetime


times=[]

#ip=get_ip_address('ens33')  
ip='osboxes'
print (ip)
db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
cursor = db.cursor()
while(1):
	cmd="tcpdump -i ens33 -xx -c1 -l -v icmp[icmptype] == icmp-echo and icmp[icmptype] != icmp-echoreply"
	result = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\t','').split('\n')
	res=[]
	ok=0
	print (result[1])
	if ip+" >" in result[1] :
		for k in range(len(times)):
			if(times[k].ip==get_stranger_ip(result[1])):
				times[k].add(int(timp.time()))
			ok=1
	response=get_stranger_ip(result[1])
	if ok==0 :
		z=0
		x=ICMP(int(timp.time()),response)
		cursor.execute("SELECT Destination FROM alerte WHERE Message='NEW IP ADDED'")
		data = list(cursor.fetchall())
		for iii in data:
			if str(iii[0]) == str(response):
				z=1
		if z==0:
			print ("UNUL NOU")
			print (result[1])
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('ICMP', 'NEW IP ADDED','LOW','"+str(response)+"','-','"+str(datetime.now())+"')")
			db.commit()
		times.append(x)
	time=result[0].split(' ')[0]
	del result[0] 	
	del result[0] 	
	for i in range(len(result)):
		try:
			res.append(result[i].split('  ')[1])
		except:
			pass            	
	values = ' '.join(str(v) for v in res)
	values=values.split(' ')
	times[len(times)-1].header.append(values[7:][:10])
	ICMP.check_header(times[len(times)-1])
	print ("DA")
	get_header_ip(values)
	if ckeck(values,16) ==  0:
		if ckeck(values,97) ==  0:
			print ('ICMP: PADDING FAILED')
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('ICMP', 'PADDING FAILED','HIGH','"+str(response)+"','"+str(''.join(values))+"','"+str(datetime.now())+"')")
			#cursor.execute("INSERT INTO icmp (ID_event,Name,Alert_Type,IP) VALUES('1', 'ICMP', 'PADDING FAILED','"+response+"' )")
			db.commit()
	print (len(times))
	
	
	
	
