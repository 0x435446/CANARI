import sys
import subprocess
import time
import os
sys.path.append('../')
from Utility import *
from Methods import *


#ip=get_ip_address('eth0')  
ip='kali'


URLS=[]
URL=''
Cookie=''
while(1):
	added=0
	added_GET=0
	cmd="tcpdump -A -s 0 'tcp dst port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'  -c 1"
	result = subprocess.check_output(cmd, shell=True).split("\n")
	for i in range(len(result)):
		result[i]=result[i].split(': ')
		if 'Agent' in result[i][0]:
			if result[i][1] != 'Chosen Agent':
				print "User-Agent ALERT!"
		if 'Cookie' in result[i][0]:
			Cookie=result[i][1]
		if 'Host' in result[i][0]:
			URL=result[i][1]
		if 'GET' in result[i][0]:
			GET=result[i][0]
			try:
				GET=GET.split('?')[1].split(' ')[0].split('&')
				for i in range(len(GET)):
					GET[i]=GET[i].split("=")
			except:
				GET=GET.split(' ')
				path=[]
				for counter in range(len(GET)):
					if "HTTP" in GET[counter]:
						path .append(GET[counter-1])
				GET=path
		if URL!='':
			if len(URLS) == 0:
				x=WEB()
				x.add(URL,Cookie,GET,str(int(time.time())))
				URLS.append(x)
			else:
				for i in range(len(URLS)):
					if added==0:
						ok=0
						if URL==URLS[i].URL:
							if added_GET==0:
								URLS[i].GET.append(GET)
								URLS[i].GET_time.append(str(int(time.time())))
								for counter in range(len(GET)):
									if len(GET)>1:
										for counter2 in range(len(GET[counter])):
											print GET[counter][counter2] + "   ---------------"
											if len(GET[counter][counter2]) > 10:
												print "ALERT! LEN GET > 10: "+ GET[counter][counter2]
									else:
										if len(GET[counter])>10:
											print "ALERT! LEN GET > 10: "+ GET[counter]
								added_GET=1
							for ii in range(len(URLS[i].Cookies)):
								ok2=0
								if URLS[i].Cookies[ii] == Cookie:
									ok2=1
							if ok2 == 0:
								URLS[i].Cookies.append(Cookie)
								URLS[i].adds+=1
								if URLS[i].adds>2:
									print "ALERT! MULTIPLE COOKIES SENT TO "+ URLS[i].URL
							ok=1
						if ok==0:
							x=WEB()
							x.add(URL,Cookie,GET,str(int(time.time())))
							URLS.append(x)
							added=1

	for i in range(len(URLS)):
		print URLS[i].URL,str(URLS[i].Cookies),str(URLS[i].GET),str(URLS[i].GET_time)





