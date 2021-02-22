from mitmproxy import http
from mitmproxy.net.http import Headers
from mitmproxy import ctx
from mitmproxy.net.http.http1.assemble import assemble_request
import time
import binwalk
import re
import sys
import base64
import MySQLdb 
sys.path.append('./modules')
from Utility import *
from Methods import *
from verify_encoding import *

def verify_content(content,url):
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	match = re.findall(r'[\w\.-]+@[\w\.-]+', content.decode('latin1'))
	if len(match)>0:
		print ("Fisier cu email-uri trimis !😍  --> ", ', '.join(match))
		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'EMAIL EXFILTRATION','MEDIUM','"+url+"','"+', '.join(match)+"','"+str(datetime.now())+"')")
		db.commit()
		print ("HTTPS EMAIL COMMITED")

	match = re.findall(r'(?=[-]*(?=[A-Z]*(?=[-])))(.*)(?=[-]*(?=[A-Z]*(?=[-])))', content.decode('latin1'))
	if len(match)>0:
		if ("RSA" in content.decode('latin1') ) or ("rsa" in content.decode('latin1')):
			print ("Fisier cu chei RSA trimis!😍  -- >", ', ',content.decode('latin1'))
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'RSA KEY EXFILTRATION','HIGH','"+url+"','"+content.decode('latin1')+"','"+str(datetime.now())+"')")
			db.commit()
			print ("HTTPS RSA COMMITED")
			
	if ("Pass" in content.decode('latin1')) or ("pass" in content.decode('latin1')) or ("PASS" in content.decode('latin1')):
		print ("Fisier cu parole trimis!😍  -- >", ', ',content.decode('latin1'))
		cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'PASSWORDS EXFILTRATION','LOW','"+url+"','"+content.decode('latin1')+"','"+str(datetime.now())+"')")
		db.commit()
		print ("HTTPS PASSWORDS COMMITED")

	db.close()

def check_whitelist(word):
	x=open("./modules/whitelist.txt","r").read().strip().split('\n')
	for i in x:
		print (word)
		if i in word:
			return 1;
	return 0;

def check_whitelist_ua(word):
	x=open("./modules/whitelist_user_agent.txt","r").read().strip().split('\n')
	for i in x:
		print ("COCOSEL",i,word)
		if i in word:
			return 1;
	return 0;


def check_get(GET,url):
	global signatures
	path=GET.split("/")
	print (path)
	path=filter(None, path)
	for i in path:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
		cursor = db.cursor()
		if verify_encoding(i) <10:
			print ("ALERTA HTTPS! UNKNOWN BASE FOUND!")
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'UNKNOWN BASE FOUND!','MEDIUM','"+url+"','"+i+"','"+str(datetime.now())+"')")
			db.commit()
			print ("HTTPS BASE COMMITED")
		if len(i) > 15:
			print ("ALERTA HTTPS! LENGTH!")
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'GET LENGTH > 15','MEDIUM','"+url+"','"+i+"','"+str(datetime.now())+"')")
			db.commit()
			print ("HTTPS LEN COMMITED")
		for k in signatures:
			if k in i:
				print ("ALERTA HTTPS! HEX SIGNATURE FOUND!")
				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'HEX SIGNATURE FOUND!','MEDIUM','"+url+"','"+i+"','"+str(datetime.now())+"')")
				db.commit()
				print ("HTTPS SIGNATURE COMMITED")
		db.close()

def request(flow: http.HTTPFlow):
	print("URL",flow.request.pretty_url)
	x=check_whitelist(flow.request.pretty_url)
	if x==0:
		if check_whitelist_ua(flow.request.headers['User-Agent']) == 0:
			print ("ALERTA HTTPS! User-Agent!")
			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('HTTPS', 'User-Agent!','MEDIUM','-','"+flow.request.headers['User-Agent']+"','"+str(datetime.now())+"')")
			db.commit()
			db.close()
			print ("HTTPS UserAgent COMMITED")
		print ("PATH:",flow.request.path)
		GET=flow.request.path
		global signatures
		signatures=read_file('signatures')
		check_get(GET,flow.request.pretty_url)
		try:
			cookies = flow.request.headers['Cookies']
		except:
			pass
		if flow.request.method == "POST" or flow.request.method == "PUT":
			ctx.log.info("Sensitive pattern found")
			flow.intercept()
			f = open("/tmp/buffer", "wb")
			content=flow.request.content
			verify_content(content,flow.request.pretty_url)
			f.write(content)
			f.close()
			for module in binwalk.scan("/tmp/buffer",signature=True,quiet=True,extract=False):
				pass
			ok=0
			for result in module.results:
				if "LZMA" not in result.description and "Zlib" not in result.description:
					print (result.description.split(',')[0])
					ok=1
			if ok==0:
				print (flow.request.text)
			print (flow.request.host_header)
			flow.resume()
			ctx.log.info("Trafic blocat")



def response(flow):
	print ("AM AJUNS AICI")
