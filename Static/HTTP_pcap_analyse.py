import subprocess
import sys


sys.path.append('../modules/')
from verify_encoding import *
import re


class PacheteHTTP():
	def __init__(self, tip, source, destination, UserAgent, GET, GETparams, Cookie, POST, payload, risk, message, timestamp):
		self.tip=tip
		self.source=source
		self.destination=destination
		self.UserAgent=UserAgent
		self.GET=GET
		self.GETparams=GETparams
		self.POST=POST
		self.payload=payload
		self.Cookie=Cookie
		self.risk=risk
		self.message=message
		self.timestamp=timestamp

	def get_pachet(self):
		return self.tip, self.source,self.destination,self.UserAgent,self.GET,self.Cookie,self.POST,self.payload,self.risk,self.message,self.timestamp

class FilesHTTP():
	def __init__(self, name, tip):
		self.name = name
		self.tip = tip

	def get_file(self):
		return self.name, self.tip

class AlerteFilesHTTP():
	def __init__(self, name, alerta, payload):
		self.name = name
		self.alerta = alerta
		self.payload = payload

	def get_alert(self):
		return self.name, self.alerta, self.payload



def checkREGEXemail(word):
	match = re.findall(r'[\w\.-]+@[\w\.-]+', word.decode('latin1'))
	if len(match)>0:
		return 1
	return 0

def checkREGEXRSA(word):
	match = re.findall(r'(?=[-]*(?=[A-Z]*(?=[-])))(.*)(?=[-]*(?=[A-Z]*(?=[-])))', word.decode('latin1'))
	if len(match)>0:
		if ("RSA" in word.decode('latin1') ) or ("rsa" in word.decode('latin1')):
			return 1
	return 0

def checkREGEXpass(word):
	if ("Pass" in word.decode('latin1')) or ("pass" in word.decode('latin1')) or ("PASS" in word.decode('latin1')):
		return 1
	return 0

def getFileName(word):
	file = open(word.encode('latin1'),'rb').read().strip().split('\n'.encode())
	filename = ''
	for i in file:
		nr = 0
		if 'Content-Disposition' in i.decode():
			try:
				filename = i.decode().split("=")[2].replace("\"",'').replace("\r","").replace("\n","")
			except:
				pass
	return filename


def checkHTTPTraffic(filename):
	output = subprocess.check_output("tcpdump -r "+filename+" 'tcp dst port http and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' -v", shell=True)
	f=output.strip().split("\n\t\n".encode())
	pachete = []
	destinatii = []
	for i in f:
		pachet = i.decode().split('\n')
		sursa = ''
		destinatie = ''
		UserAgent = ''
		GET = ''
		POST = ''
		timestamp = ''
		Cookie = ''
		for j in range(len(pachet)):
			if j == 0:
				timestamp = pachet[j].split(' ')[0]
			if j == 1:
				splited = pachet[j].split(' ')
				for k in range(len(splited)):
					if splited[k] == '>':
						sursa = '.'.join(splited[k-1].split('.')[:-1])
			if j > 1:
				if "GET" in pachet[j]:
					GET = pachet[j].split(' ')[1]
				if "User-Agent" in pachet[j]:
					UserAgent = pachet[j].split(': ')[1]
				if "Host" in pachet[j]:
					destinatie = pachet[j].split(': ')[1]
					destinatii.append(pachet[j].split(': ')[1])
				if "Cookie" in pachet[j]:
					Cookie = pachet[j].split(': ')[1].split('; ')
				if "POST" in pachet[j]:
					POST = "FILE"


		try:
			parametriiGET = GET.split('?')[1]
			GETs = parametriiGET.split('&')
		except:
			GETs=[]
		x = PacheteHTTP('HTTP', sursa, destinatie, UserAgent, GET.split("?")[0], GETs, Cookie, POST, "", "","HTTP Exfiltration",timestamp)
		pachete.append(x)

	de_printat = []
	for i in pachete:
		for j in i.GETparams:
			param = j.split("=")
			if len(param) == 1:
				pachet_nou = PacheteHTTP(i.tip, i.source, i.destination, i.UserAgent,i.GET,i.GETparams,i.POST, i.Cookie,i.payload,i.risk,i.message,i.timestamp)
				pachet_nou.message = "Inconsistent GET parameter"
				pachet_nou.risk = "HIGH"
				pachet_nou.payload = param[0]
				de_printat.append(pachet_nou)
			else:
				if verify_encoding(param[1]) < 10:
					pachet_nou2 = PacheteHTTP(i.tip, i.source, i.destination, i.UserAgent,i.GET,i.GETparams,i.POST, i.Cookie,i.payload,i.risk,i.message,i.timestamp)
					pachet_nou2.message = "GET UNKNOWN BASE FOUND"
					pachet_nou2.risk = "MEDIUM"
					pachet_nou2.payload = param[1]
					de_printat.append(pachet_nou2)
		if len(i.GET) > 15:
			pachet_nou3 = PacheteHTTP(i.tip, i.source, i.destination, i.UserAgent,i.GET,i.GETparams,i.POST, i.Cookie,i.payload,i.risk,i.message,i.timestamp)
			pachet_nou3.message = "GET LENGTH "
			pachet_nou3.risk = "LOW"
			pachet_nou3.payload = GET
			de_printat.append(pachet_nou3)
		if len(i.POST) >1:
			pachet_nou4 = PacheteHTTP(i.tip, i.source, i.destination, i.UserAgent,i.GET,i.GETparams,i.POST, i.Cookie,i.payload,i.risk,i.message,i.timestamp)
			pachet_nou4.message = "FILE SENT!"
			pachet_nou4.risk = "HIGH"
			pachet_nou4.payload = "File"
			de_printat.append(pachet_nou4)

	output = subprocess.check_output("tshark -q -r "+filename+" --export-objects 'http,ExtractedFiles/Temporar' ", shell=True)
	output = subprocess.check_output("file ExtractedFiles/Temporar/*", shell=True)
	files = []
	for i in output.split('\n'.encode()):
		if len(i.decode())>1:
			if "HTML document".encode() not in i:
				if "XML".encode() not in i:
					x = FilesHTTP(i.decode().split(':')[0], i.decode().split(':')[1])
					files.append(x)

	alerts = []
	for i in range(len(files)):
		try:
			content = open(files[i].get_file()[0], "rb").read().strip()
			filename2 = getFileName(files[i].get_file()[0])
			if filename2 == '':
				filename2 = files[i].get_file()[0].split("/")[len(files[i].get_file()[0].split("/"))-1]
			if checkREGEXemail(content) == 1:
				alerts.append(AlerteFilesHTTP(filename2, "Email found!", content.decode()))
			if checkREGEXRSA(content) == 1:
				alerts.append(AlerteFilesHTTP(filename2, "RSA file found!", content.decode()))
			if checkREGEXpass(content) == 1:
				alerts.append(AlerteFilesHTTP(filename2, "Password found!", content.decode()))
			files[i].name = filename2
		except:
			pass

	try:
		output = subprocess.check_output("rm ExtractedFiles/Temporar/*", shell=True)
	except:
		pass
	destinatii = list(set(destinatii))
	return de_printat, files, alerts, destinatii