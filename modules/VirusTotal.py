from vt import *
import json

def init():
	vt = VT()
	vt.setkey('03b3cc1de70a217d05e42394628e25971dbff611301f5efdb1c5188523f3bd66')
	return vt

def search_url(URL):
	for_return=[]
	vt=init()
	#print (vt.geturl("https://posta-romania.com/"))
	try:
		response=vt.geturl(URL)
		response=response['scans']
		for i,j in response.items():
			aux=[]
			if j['detected'] == True:
				aux.append(i)
				aux.append(j['detected'])
				aux.append(j['result'])
				for_return.append(aux)
	except:
		for_return=[]
		pass
	return for_return
