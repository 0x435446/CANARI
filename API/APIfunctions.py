import socket
import sys
import MySQLdb 
from datetime import datetime



def getHTTPSdatas():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 9870)
	sock.connect(server_address)
	data = sock.recv(999)
	return data.decode()


def getICMPdatas():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 9871)
	sock.connect(server_address)
	data = sock.recv(999)
	return data.decode()


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

def insertIntoDatabase(Type,Message,Risk,Source,Destination,Payload):
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("INSERT INTO alerte (Type,Message,Risk,Source,Destination,Payload,Timestamp) VALUES('"+Type+"', '"+Message+"','"+Risk+"','"+Source+"','"+Destination+"','"+Payload+"','"+str(datetime.now())+"')")
	db.commit()