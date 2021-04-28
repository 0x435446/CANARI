from base64 import * 


def netbios_encode(input_string):
	return ''.join([chr((ord(c)>>4)+ord('A'))+chr((ord(c)&0xF)+ord('A')) for c in input_string])

d={}
def initializare():
	global d
	data = open( './modules/Data_encoding/probabilitati.txt' ).read().split('\n')
	for i in range(len(data)):
		try:
			data[i]=data[i].split(':')
			d[data[i][0]]=data[i][1]
		except:
			pass




def verify_encoding(word):
	global d
	initializare()
	suma=0
	nr=0
	for i in range(len(word)-1):
		try:
			nr+=1
			grup=word[i]+word[i+1]
			if d[grup]:
				suma+=int(d[grup])
		except:
			pass
	try:
		return suma/nr
	except:
		pass

def verify_encoding_API(word, location):
	e={}
	data = open( location ).read().split('\n')
	for i in range(len(data)):
		try:
			data[i]=data[i].split(':')
			e[data[i][0]]=data[i][1]
		except:
			pass
	suma=0
	nr=0
	for i in range(len(word)-1):
		try:
			nr+=1
			grup=word[i]+word[i+1]
			if e[grup]:
				suma+=int(e[grup])
		except:
			pass
	try:
		return suma/nr
	except:
		pass
