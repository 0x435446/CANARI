import sys
import subprocess
sys.path.append('../')
from Utility import *
from Methods import *
import MySQLdb 
from datetime import datetime
import socket
import _thread



def getPacketDetails():
	HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
	PORT = 9871        # Port to listen on (non-privileged ports are > 1023)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (HOST, PORT)
	sock.bind(server_address)
	sock.listen(1)

	while True:
		global timeAPI
		global destinationAPI
		global sourceAPI
		global paddingAPI
		ceva = [sourceAPI, destinationAPI, ''.join(paddingAPI), timeAPI]
		connection, client_address = sock.accept()
		try:
			while True:
				connection.sendall('|'.join(ceva).encode())
				break;

		finally:
			connection.close()


def check_whitelist(word,path):
	x=open(path,"r").read().strip().split('\n')
	if path == "./modules/Filters/whitelist_sources.txt":
		for i in x:
			if i in word:
				return 1
	return 0;



global timeAPI
timeAPI = ''
global destinationAPI
destinationAPI = ''
global sourceAPI
sourceAPI = ''
global paddingAPI
paddingAPI = ''




def icmp_start():
	for_test=0
	times=[]
	ip=get_ip_address('ens33')  
	#ip='osboxes'
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	global start_icmp
	start_icmp=1
	global timeAPI
	global destinationAPI
	global sourceAPI
	global paddingAPI
	_thread.start_new_thread(getPacketDetails,())
	while(start_icmp!=0):
		cmd="sudo tcpdump -i ens33 -xx -c1 -l -v icmp[icmptype] == icmp-echo and icmp[icmptype] != icmp-echoreply 2>/dev/null"
		result = subprocess.check_output(cmd, shell=True).decode('utf-8')
		search= result.split(' ')
		host=''
		for i in range(len(search)-2):
			if search[i] == '>':
				host = search[i-1]
				break;
		if check_whitelist(host,"./modules/Filters/whitelist_sources.txt") == 0:
			sourceAPI = host
			timeAPI = str(int(timp.time()))
			result = result.replace('\t','').split('\n')
			res=[]
			ok=0
			if (" >" in result[1]) :
				for k in range(len(times)):
					if(times[k].ip==get_stranger_ip(result[1])):
						times[k].add(int(timp.time()))
					ok=1
			response=get_stranger_ip(result[1])
			destinationAPI = response
			if ok==0 :
				z=0
				x=ICMP(int(timp.time()),response,host)
				if for_test==0:
					cursor.execute("SELECT Destination FROM alerte WHERE Message='NEW IP ADDED'")
					data = list(cursor.fetchall())
				for iii in data:
					if str(iii[0]) == str(response):
						z=1
				if z==0:
					if for_test==0:
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('ICMP', 'NEW IP ADDED','LOW','"+host+"','"+str(response)+"','-','"+str(datetime.now())+"')")
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
			paddingAPI = values
			times[len(times)-1].header.append(values[7:][:10])
			ICMP.check_header(times[len(times)-1])
			get_header_ip(values)
			print ("AICI SUNT VALUES",values)
			if ckeck(values,16) ==  0:
				if ckeck(values,97) ==  0:
					print ('ICMP: PADDING FAILED')
					if for_test==0:
						cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('ICMP', 'PADDING FAILED','HIGH','"+host+"','"+str(response)+"','"+str(''.join(values))+"','"+str(datetime.now())+"')")
					#cursor.execute("INSERT INTO icmp (ID_event,Name,Alert_Type,IP) VALUES('1', 'ICMP', 'PADDING FAILED','"+response+"' )")
						db.commit()
			print (len(times))
	
	
	

def stop_icmp():
	global start_icmp
	start_icmp=0

if len(sys.argv)>1:
	if sys.argv[1] == 'a':
		icmp_start()