import sys
import subprocess
import time
import os
sys.path.append('../')
from Utility import *
from Methods import *




open_ports=[]

while(1):
	cmd="netstat -tulpn"
	result = subprocess.check_output(cmd, shell=True).split('\n')
	for i in range(2,len(result)):
		if len(result[i])<2:
			del result[i]
		else:
			result[i]=result[i].split(' ')
			while("" in result[i]) : 
				result[i].remove("") 
			x=CONNECTIONS()
			port=result[i][3].split(':')[1]
			PID=result[i][6]
			if PID != '-':
				timp=time.time()
				ok=0
				ok2=0
				if len(open_ports)==0:
					x.add(port,PID,str(int(time.time())))
					open_ports.append(x)
				else:
					for ii in range(len(open_ports)):
						if open_ports[ii].PID == PID:
							for k in range(len(open_ports[ii].ports)):
								if open_ports[ii].ports[k]==port:
									ok=1
							if ok==0:
								open_ports[ii].ports.append(port)
								open_ports[ii].unchanged=1
							ok2=1
					if ok2==0:
						x.add(port,PID,str(int(time.time())))
						open_ports.append(x)

	for i in range(len(open_ports)):
		if open_ports[i].unchanged==1:
			print "PID --- "+open_ports[i].PID+" --- "+str(open_ports[i].ports)+" --- "+str(open_ports[i].time)
			open_ports[i].unchanged=0
