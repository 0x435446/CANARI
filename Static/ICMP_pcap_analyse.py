import subprocess
import sys
import datetime

sys.path.append('../modules/')
from Utility import *


class PacheteICMP():
	def __init__(self):
		self.sursa=''
		self.destinatie=[]
		self.padding=[]
		self.timestamp=[]

class AlerteICMP():
	def __init__(self, tip, sursa, destinatie, payload, message):
		self.tip=tip
		self.sursa=sursa
		self.destinatie=destinatie
		self.payload=payload
		self.message=message

	def getItems(self):
		return self.sursa, self.destinatie, self.payload, self.message

datas = []
def checkICMPTraffic(filepath):
	output = subprocess.check_output("tcpdump -r "+filepath+" -l -xx icmp[icmptype] == icmp-echo and icmp[icmptype] != icmp-echoreply 2>/dev/null", shell=True)
	pachete = output.decode().split('\n')
	new = []
	pacheteICMP = []
	for i in pachete:
		if len(new) > 0:
			if len(i) > 0:
				if i[0] == '\t':
					new.append(i)
				else:
					datas.append(new)
					new = []
					new.append(i)
		else:
			new.append(i)
	for i in datas:
		lines = []
		bucatele = i[0].split(' ')
		timestamp = bucatele[0].split('.')[0]
		sursa = '' 
		destinatie =''
		for j in range(len(bucatele)):
			if bucatele[j] == '>':
				sursa = bucatele[j-1]
				destinatie = bucatele[j+1].replace(":","")
		for k in range(1,len(i)):
			line = i[k].replace('\t','').split(":  ")[1].split(' ')
			lines.append(' '.join(line))

		padding = ' '.join(lines).split(' ')
		ok = 0
		index = -1
		for i in range(len(pacheteICMP)):
			if pacheteICMP[i].sursa == sursa:
				ok = 1
				index = i
				break;
		if ok == 1:
			pacheteICMP[index].destinatie.append(destinatie)
			pacheteICMP[index].padding.append(padding)
			pacheteICMP[index].timestamp.append(timestamp)
		else:
			x = PacheteICMP()
			x.tip="ICMP"
			x.sursa=sursa
			x.destinatie.append(destinatie)
			x.padding.append(padding)
			x.timestamp.append(timestamp)
			pacheteICMP.append(x)

	alerteICMP = []

	destinatii = []

	for i in pacheteICMP:
		lista_destinatii = []
		dest = '' 
		for j in range(len(i.destinatie)):
			lista_timestamp = []
			if i.destinatie[j] in lista_destinatii:
				break;
			else:
				dest = i.destinatie[j]
				for k in range(len(i.timestamp)):
					if i.destinatie[k] == i.destinatie[j]:
						lista_timestamp.append(i.timestamp[k])
			lista_destinatii.append(dest)
			diferente = []
			for l in range(0, len(lista_timestamp)-4):
				try:
					format = '%H:%M:%S'
					startDateTime = datetime.strptime(lista_timestamp[l],format)
					endDateTime = datetime.strptime(lista_timestamp[l+4],format)
					diff = endDateTime - startDateTime
					diferente.append(diff)
				except:
					pass
			for k in diferente:
				if "0:00:" == str(k)[:5].strip():
					destinatii.append(i.destinatie[j])
					z = AlerteICMP('ICMP', i.sursa,i.destinatie[j],'','ICMP FREQUENCY')
					alerteICMP.append(z)


	payloads = {}
	for i in pacheteICMP:
		for k in range(len(i.destinatie)):
			if (ckeck(i.padding[k],16) == 0):
				if(ckeck(i.padding[k],97) == 0):
					ret = ''.join(i.padding[k])[116:]
					if i.destinatie[k] in payloads.keys():
						payloads[i.destinatie[k]] = payloads[i.destinatie[k]] + ret
					else:
						payloads[i.destinatie[k]] = ret
					destinatii.append(i.destinatie[k])
					alerta1 = AlerteICMP('ICMP', i.sursa, i.destinatie[k], ret, "PADDING FAILED")
					alerteICMP.append(alerta1)

	destinatii = list(set(destinatii))
	print (destinatii)
	return alerteICMP, destinatii, payloads


