import subprocess
import sys
from verify_encoding import *
sys.path.append('./Static/MachineLearning')
import verify_enc
import predict
sys.path.append('../modules')
import Utility


class Pachete():
	def __init__(self, tip, source, destination, payload, risk, message, timestamp):
		self.tip=tip
		self.source=source
		self.destination=destination
		self.payload=payload
		self.risk=risk
		self.message=message
		self.timestamp=timestamp

	def get_pachet(self):
		return self.tip, self.source,self.destination,self.payload,self.risk,self.message,self.timestamp

def checkTrafficDNS(Filename):
	output = subprocess.check_output("tcpdump -r "+Filename+" port 53", shell=True)
	source = []
	destination = []
	payload = []
	timestamp = []
	d={}
	d=verify_enc.initializare(d)

	f=output.strip().split("\n".encode())
	for i in f:
		line = i.split(" ".encode())
		for j in range(len(line)):
			ok = 0
			line[j]=line[j].decode()
			if line[j] == "A?" or line[j] == "AAAA" or line[j] == "TXT?":
				if ":".encode() not in line[j+1]:
					timestamp.append(line[0])
					ok = 1
					word = line[j+1].replace("www".encode(),"".encode())
					if chr(word[-1]) == '.':
						destination.append(word[:-1].decode())
						payload.append('.'.join(word[:-1].decode().split('.')[:-2]))
					elif chr(word[-1]) == ',':
						destination.append(word[:-2].decode())
						payload.append('.'.join(word[:-2].decode().split('.')[:-2]))
					else:
						destination.append(word.decode())
						payload.append('.'.join(word.decode().split('.')[:-2]))
			if line[j] == '>':
				sursa = line[j - 1]
			if ok == 1:
				source.append('.'.join(sursa.split('.')[:-1]))

	pachete = []

	for i in range(len(destination)):
		tip=''
		dest = ''
		payl = ''
		message = ''
		risk = ''
		tt = ''
		if destination[i][0] == '.':
			dest = destination[i][1:]
		else:
			dest = destination[i]
		if payload[i] == '':
			payl='None'
		else:
			payl=payload[i]
		if len(payload[i])<4:
			message="Posibil ads"
		else:
			message="DNS Exfiltration"
		risk = "Unknown"
		tt = timestamp[i]
		pack = Pachete(tip, source[i], dest, payl, risk, message, tt)
		pachete.append(pack)




	dest = []
	for i in range(len(destination)):
		dest.append(destination[i].replace(payload[i]+'.',''))

	#print ("Numar de request-uri DNS:",len(source))
	#print ("Numar de domenii diferite:",len(list(set(dest))))


	lista = []
	de_printat=[]
	lista = []
	lista2=[]


	for i in range(len(pachete)):
		if pachete[i].payload != 'None':
			if pachete[i].payload not in lista:
				raspuns_ML = predict.check_model_4(pachete[i].payload.replace('-',''),d)
				if raspuns_ML == 0:
					pachete[i].tip ='Machine Learning'

					pachet = Pachete(pachete[i].tip, pachete[i].source, pachete[i].destination, pachete[i].payload, pachete[i].risk, pachete[i].message, pachete[i].timestamp)
					lista.append(pachete[i].payload)
					de_printat.append(pachet)

					if pachete[i].payload not in lista2:
						bucatele = pachete[i].payload.split('.')
						for k in bucatele:
							if len(k) > 2:
								try:
									if verify_encoding(pachete[i].payload) < 10:
										pachete[i].tip ='DNS'
										pachete[i].message = "UNKNOWN BASE FOUND"
										pachete[i].risk = "HIGH" 
										lista2.append(pachete[i].payload)
										de_printat.append(pachete[i])
								except:
									pachete[i].tip ='DNS'
									pachete[i].message = "UNKNOWN BASE FOUND"
									pachete[i].risk = "HIGH" 
									lista2.append(pachete[i].payload)
									de_printat.append(pachete[i])
									pass

						if pachete[i].destination.count('.') < 2:
							pachete[i].tip ='DNS'
							pachete[i].message = "DIG EXFILTRATION"
							pachete[i].risk = "HIGH" 
							lista2.append(pachete[i].payload)
							de_printat.append(pachete[i])

						if len(pachete[i].payload) > 10:
							pachete[i].tip ='DNS'
							pachete[i].message = "DNS EXFILTRATION LEN"
							pachete[i].risk = "HIGH" 
							lista2.append(pachete[i].payload)
							de_printat.append(pachete[i])

	return len(source),list(set(dest)),len(list(set(dest))),de_printat
