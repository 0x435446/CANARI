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



def read_rules():
	x=open('./modules/Rules/rules.txt','r').read().strip().split("\n")
	n = len(x)
	for i in range(n):
		if x[i][0] == b'#':
			del x[i]
		if x[i].count(':') != 7:
			del x[i]
	for i in range(len(x)):
		x[i] = x[i].split(':')
	return x

def check_rules(TIP,pachet):
	try:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
		cursor = db.cursor()
		if TIP == "HTTP":
			rules=read_rules()
			HOST=''
			DESTINATION=''
			USER_AGENT=''
			hexa=[]
			result = pachet
			visible = result.split('\n\t\n\t')[0]
			invisible = result.split('\n\t\n\t')[1]
			visible = visible.replace('\t','').split('\n')
			invisible = invisible.replace('\t','').split('\n')
			visible[1]=visible[1].split(' ')
			for i in range(len(visible[1])):
				if visible[1][i] == '>':
					HOST = visible[1][i-1].split('.')
					del HOST[-1]
					HOST='.'.join(HOST)
					break
			for i in range(2,len(visible)):
				if visible[i].split(': ')[0] == 'User-Agent':
					USER_AGENT = visible[i].split(': ')[1]
				if visible[i].split(': ')[0] == 'Host':
					DESTINATION = visible[i].split(': ')[1]
			for i in range(len(invisible)):
				try:
					hexa.append(invisible[i].split(':  ')[1])
				except:
					pass
			content = ''.join(hexa).replace(' ','')
			for i in range(len(rules)):
				ok_host = 0
				ok_destination = 0
				ok_user_agent = 0
				if rules[i][0] == 'HTTP':
					if rules[i][1] == '*':
						ok_host = 1
					elif rules[i][1] == HOST:
						ok_host = 1
					if rules[i][2] == '*':
						ok_destination = 1
					elif rules[i][2] == DESTINATION:
						ok_destination = 1
					if rules[i][3] == '*':
						ok_user_agent = 1
					elif rules[i][3] == USER_AGENT:
						ok_user_agent = 1
					if (ok_user_agent == 1) and (ok_destination == 1) and (ok_host == 1):
						if content[int(rules[i][4]):][:len(rules[i][5].strip())] == rules[i][5].strip():
							cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTP', '"+rules[i][7]+"','"+rules[i][6]+"','"+DESTINATION+"','"+rules[i][5].strip()+"','"+str(datetime.now())+"')")
							db.commit()
							print ("COMMITED HTTP")
			return HOST

		if TIP == "DNS":
			new_pachet=[]
			HOST=''
			DESTINATION=''
			rules=read_rules()
			pachet = pachet.split('\n\t')
			search = pachet[0].replace('\t','').split(' ')
			for i in range(len(search)-1):
				if search[i] == '>':
					HOST = search[i-1].split('.')
					del HOST[-1]
					HOST='.'.join(HOST)
					break
			for i in range(len(search)-1,0,-1):
				if search[i].count('.')>1 and len(search[i])>2:
					DESTINATION=search[i]
					break;
			del pachet[0]
			for i in range(len(pachet)):
				pachet[i]=pachet[i].split(':  ')
				new_pachet.append(pachet[i][1].replace('\n','').replace(' ',''))
			for i in range(len(rules)):
				ok_host = 0
				ok_destination = 0
				ok_user_agent = 0
				if rules[i][0] == 'DNS':
					if rules[i][1] == '*':
						ok_host = 1
					elif rules[i][1] == HOST:
						ok_host = 1
					if rules[i][2] == '*':
						ok_destination = 1
					elif rules[i][2] == DESTINATION:
						ok_destination = 1
					if (ok_destination == 1) and (ok_host == 1):
						if ''.join(new_pachet)[int(rules[i][4]):][:len(rules[i][5].strip())] == rules[i][5].strip():
							cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', '"+rules[i][7]+"','"+rules[i][6]+"','"+DESTINATION+"','"+rules[i][5].strip()+"','"+str(datetime.now())+"')")
							db.commit()
							print ("COMMITED DNS")
			return HOST
	except:
		pass