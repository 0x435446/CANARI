import subprocess
import sys
output = subprocess.check_output("tcpdump -r Traffic/trafic_Catalin.pcapng 'tcp dst port http and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' -v", shell=True)



source = []
destination = []
payload = []
timestamp = []
f=output.strip().split("\n\t\n".encode())
for i in f:
	pachet = i.decode().split('\n')
	sursa = ''
	destinatie = ''
	UserAgent = ''
	GET = ''
	POST = ''
	timestamp = ''
	for j in range(len(pachet)):
		print (pachet[j])
		if j == 0:
			timestamp = pachet[j].split(' ')[0]
		if j == 1:
			splited = pachet[j].split(' ')
			for k in range(len(splited)):
				if splited[k] == '>':
					sursa = splited[k-1]
		if j>1:
			if "GET" in pachet[j]:
				GET = pachet[j].split(' ')[1]
			if "User-Agent" in pachet[j]:
				UserAgent = pachet[j].split(': ')[1]
			if "Host" in pachet[j]:
				destinatie = pachet[j].split(': ')[1]
	print (sursa,destinatie,UserAgent,GET,timestamp)
