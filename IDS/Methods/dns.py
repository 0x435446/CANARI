import sys
import subprocess
import time
sys.path.append('../')
from Utility import *
from Methods import *
from Crypto.Util.number import long_to_bytes

from urlparse import urlparse



def read_file(fisier):
	x=[]
	if fisier == 'TLD':
		filepath = '../TLD/IANA.txt'
	else:
		filepath = '../Magic_Numbers/signatures.txt'
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		while line:
			x.append(line.strip())
			line = fp.readline()
			cnt += 1
	return x



times=[]

def check_chars(word):
	for i in range(len(word)):
		if ord(word[i])<=ord('0') or ord(word[i]) >=ord('z'):
			return 1
	return 0



ip=get_ip_address('eth0')  
tld=read_file('TLD')
signatures=read_file('signatures')

database=[]


while(1):
	cmd="tcpdump -i eth0 -c1 -l -v -n -t port 53"
	result = subprocess.check_output(cmd, shell=True).replace('\t','').split('\n')
	res = []
	result[1]=result[1].split()
	for val in result[1]: 
		if val != None : 
			res.append(val) 
	url=res[5].split('.')
	for i in range(len(url)):
		if url[i]==None:
			del url[i]
	bd=url
	for i in range(len(tld)):
		tld[i]=tld[i].lower()
	for i in range(len(url)):
		for j in range(len(tld)):
			try:
				if url[i]==tld[j]:
					del url[i]
				if url[i]=="www":
					del url[i]
					del bd[i]
			except:
				pass
	print bd[len(bd)-2]
	ok=0
	if len(bd)>2:
		for i in range(len(database)):
			if(database[i].check(bd[len(bd)-2])==1):
				for j in range(len(bd)-2):
					if len(str(bd[j])) > 10:
						print "ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j])))
					if check_chars(bd[j]) == 0:
						print "ALERT! DNS EXFILTRATION NONASCII CHARS - " + bd[j]
					kappa.add(bd[j],int(time.time()))
				ok=1

		if ok==0:
			print "Domain added! "+ bd[len(bd)-2]
			kappa=DNS(bd[len(bd)-2])
			for j in range(len(bd)-2):
				kappa.add(bd[j],int(time.time()))
				if len(str(bd[j])) > 10:
					print "ALERT! DNS EXFILTRATION LEN - "+ str(len(str(bd[j])))
				if check_chars(bd[j]) == 1:
					print "ALERT! DNS EXFILTRATION NONASCII CHARS" + bd[j]
			database.append(kappa)

	for i in range(len(database)):
		print database[i].d,database[i].sd
		for j in range(len(database[i].sd)):
			try:
				for k in signatures:
					if k in database[i].sd[j]:
						print "ALERT! DNS EXFILTRATION - " + str(k)
			except:
				pass


