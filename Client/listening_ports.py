import socket
import sys
import subprocess
import time
import os
import hashlib
#sys.path.append('../')
from Utility import *
from Methods import *


open_ports=[]

def hash(for_sha):
	cuvant = for_sha.encode()
	i = 0
	ok = 1
	while(ok):
		sha = hashlib.sha256((cuvant.decode()+str(i)).encode()).hexdigest()
		if sha[:3] == '000':
			print (sha)
			print (cuvant.decode()+str(i))
			ok = 0
		i += 1
	return sha+"|"+cuvant.decode()+str(i-1)


def check_pipe():
	f=open("pipe.txt","r")
	text=f.read().strip()
	f.close()
	if len(text)>1:
		return text
	else:
		return "Nope"


def connect(message):
	global word
	sock = socket.create_connection(('localhost', 1234))
	sock.sendall(message.encode())
	data = sock.recv(1000)
	print (data)
	word = data.decode()
	f=open("pipe.txt","w")
	f.write(data.decode())
	f.close()
	sock.close()

global word
content = check_pipe()
if content == "Nope":
	connect('Listen')
	print ("PRIMUL CONNECT:",word)
else:
	word = content


while(1):
	cmd="netstat -tulpn 2>/dev/null"
	result = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')
	for i in range(2,len(result)):
		if len(result[i])<2:
			del result[i]
		else:
			result[i]=result[i].split(' ')
			while("" in result[i]) : 
				result[i].remove("") 
			x=CONNECTIONS()
			port=result[i][3].split(':')[1]
			try:
				PID=result[i][6]
				if PID != '-':
					timp=time.time()
					ok=0
					ok2=0
					if len(open_ports)==0:
						x.add(port,PID,str(int(time.time())))
						open_ports.append(x)
					else:
						for ii in range(len(open_ports)):
							if open_ports[ii].PID == PID:
								for k in range(len(open_ports[ii].ports)):
									if open_ports[ii].ports[k]==port:
										ok=1
								if ok==0:
									open_ports[ii].ports.append(port)
									open_ports[ii].unchanged=1
								ok2=1
						if ok2==0:
							x.add(port,PID,str(int(time.time())))
							open_ports.append(x)
			except:
				pass

	for i in range(len(open_ports)):
		if open_ports[i].unchanged == 1:
			for_send=hash(word)
			print (for_send+"|PID --- "+open_ports[i].PID+" --- "+str(open_ports[i].ports)+" --- "+str(open_ports[i].time))
			connect(for_send+"|"+open_ports[i].PID+"-"+str(' '.join(open_ports[i].ports))+"-"+str(' '.join(open_ports[i].time))+"-LISTEN")
			open_ports[i].unchanged = 0