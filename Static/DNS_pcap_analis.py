import subprocess
import sys
output = subprocess.check_output("tcpdump -r trafic_Catalina.pcapng port 53", shell=True)
sys.path.append('./MachineLearning')
import predict


source = []
destination = []
payload = []
timestamp = []
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
print (len(source),len(destination),len(payload),len(timestamp))
for i in range(len(destination)):
	pachet = []
	pachet.append(source[i])
	if destination[i][0] == '.':
		pachet.append(destination[i][1:])
	else:
		pachet.append(destination[i])
	if payload[i] == '':
		pachet.append('None')
	else:
		pachet.append(payload[i])
	pachet.append(timestamp[i])
	pachete.append(pachet)

dest = []
for i in range(len(destination)):
	dest.append(destination[i].replace(payload[i],''))
print (len(list(set(dest))))


lista = []

de_printat=[]
lista = []
for i in range(len(pachete)):
	if pachete[i][2] != 'None':
		if pachete[i][2] not in lista:
			raspuns_ML = predict.check_model_3(pachete[i][2].replace('-',''))
			if raspuns_ML == 0:
					lista.append(pachete[i][2])
					de_printat.append(pachete[i])

for i in de_printat:
	print (' '.join(i))
