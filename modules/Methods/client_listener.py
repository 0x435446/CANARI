import subprocess
import _thread
import socket
import sys
import hashlib
import MySQLdb 
from datetime import datetime
#sys.path.append('./modules')
sys.path.append('../')
from Client import Client



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1234)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)
sock.listen(1)
c=[]
db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
cursor = db.cursor()
def l1():
	while True:
		global c
		cmd="head -c 500 /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-' | fold -w 15 | head -n 1"
		random_bytes=subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
		print (random_bytes)
		connection, client_address = sock.accept()
		try:
			print('connection from', client_address, file=sys.stderr)
			data = connection.recv(10000).split(b"|")
			print ("DATA BA:",data)
			if len(c) == 0:
				x = Client(client_address[0])
				x.words.append(random_bytes)
				c.append(x)
				print('received "%s"' % data, file=sys.stderr)
				connection.sendall(random_bytes.encode())
			else:
				ok = 0
				ok2 = 0
				for i in range(len(c)):
					if ok2 == 0:
						if c[i].ip == client_address[0]:
							ok2 = 1
							#try:
							data[1] = data[1].strip()
							print ("WORDS[i]:",c[i].words[c[i].index])
							print ("DATA[1]:",data[1].decode())
							if c[i].words[c[i].index] in data[1].decode():
								print ("SHA(DATA[1])",hashlib.sha256(data[1]).hexdigest())
								print ("SHA-ul trimis: ",data[0].decode())
								if (hashlib.sha256(data[1]).hexdigest() == data[0].decode()):
									if data[0].decode()[:3] == '000':
										c[i].words.append(random_bytes)
										c[i].index+=1
										print ("APROAPE AM AJUNS")
										print ("MESAJ:",data[2])
										print (type(data[2].split(b"-")[0]))
										print ("TYPE",data[2].split(b"-")[3])
										if data[2].split(b"-")[3] == b'LISTEN':
											print ("LISTEN ADAUGAT")
											cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('Listening', '"+ data[2].split(b'-')[0].decode()+" "+data[2].split(b'-')[2].decode()+"','MEDIUM','"+ data[2].split(b'-')[1].decode()+"','-','"+str(datetime.now())+"')")
											db.commit()
										if data[2].split(b"-")[3] == b'SOCKET':
											print ("SOCKET ADAUGAT")
											cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('Connections', '"+ data[2].split(b'-')[0].decode()+" "+(data[2].split(b'-')[2].decode()).replace(' ','')+"','MEDIUM','"+ data[2].split(b'-')[1].decode()+"','-','"+str(datetime.now())+"')")
											db.commit()
										print ("AM AJUNS")
										connection.sendall(random_bytes.encode())
										connection.close()
										break;
									else:
										print ("ZEROURI")
										connection.sendall(b"MUIE MA de la ZEROURI")
										connection.close()
										break;
								else:
									print ("HASH GRESIT")
									print ("DATA[1]:",data[1])
									print ("Sha data[1]:",hashlib.sha256(data[1]).hexdigest())
									print ("Sha primit:",data[0])
									connection.sendall(b"MUIE MA de la HASH")
									connection.close()
									ok = 1
									break;
							else:
								print ("NU SE AFLA IN PACHET")
								connection.sendall(b"MUIE MA de la PACHET")
								connection.close()
								break;
							'''
							except:
								connection.sendall(b"MUIE MA de la MINE")
								connection.close()
								pass
							'''
						else:
							if ok == 0:
								print ("Sal")
								x = Client(client_address[0])
								x.words.append(random_bytes)
								c.append(x)
								print('received "%s"' % data, file=sys.stderr)
								connection.sendall(random_bytes.encode())
								break;
		finally:
			connection.close()
print('waiting for a connection', file=sys.stderr)
# Wait for a connection
_thread.start_new_thread(l1,())

global a
a=[]
wait=0
while True:
	wait+=1

