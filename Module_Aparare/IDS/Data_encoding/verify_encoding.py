from base64 import * 


def netbios_encode(input_string):
	return ''.join([chr((ord(c)>>4)+ord('A'))+chr((ord(c)&0xF)+ord('A')) for c in input_string])

def initializare():
	d={}
	data = open( 'probabilitati.txt' ).read().split('\n')
	for i in range(len(data)):
		try:
			data[i]=data[i].split(':')
			d[data[i][0]]=data[i][1]
		except:
			pass

def verify_encoding(word):
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
			print suma/nr,
		except:
			pass
