import socket
import sys



def getDNSdatas():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 9872)
	sock.connect(server_address)
	data = sock.recv(999)
	return data.decode()



def getHTTPdatas():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 9873)
	sock.connect(server_address)
	data = sock.recv(999)
	return data.decode()