import sys
import subprocess
import time
import os
sys.path.append('../')
from Utility import *
from Methods import *



PIDS=[]

while(1):
	cmd="ss -4 -p"
	result = subprocess.check_output(cmd, shell=True)
	result=result.split('\n')
	for i in range(1,len(result)):
		result[i]=result[i].split(' ')
		while("" in result[i]) : 
			result[i].remove('') 
		try:
			local=result[i][4].split(":")[1]
			remote=result[i][5].split(":")[1]
			PID=result[i][6][8:][:-2].split(",")[1]
			app=result[i][6][8:][:-2].split(",")[0].replace("\"","")
			x=SOCKETS()
			if local.isdigit():
				if len(PIDS)==0:
					x.add(local,remote,PID,app,str(int(time.time())))
					PIDS.append(x)
				else:
					ok2=0
					for ii in range(len(PIDS)):
						ok=0
						if PIDS[ii].PID==PID:
							for iii in range(len(PIDS[ii].local)):
								if local==PIDS[ii].local[iii]:
									ok=1
							if ok == 0:
								PIDS[ii].local.append(local)
								PIDS[ii].unchanged=1
								print "ALERT! APLICATIA: "+PIDS[ii].app+" DESCHIDE MULTIPLE ( "+str(len(PIDS[ii].local))+" ) PORTURI, PID: "+PIDS[ii].PID
							ok2=1
					if ok2==0:
						x.add(local,remote,PID,app,str(int(time.time())))
						PIDS.append(x)

		except:
			pass
	for i in range(len(PIDS)):
		if(PIDS[i].unchanged==1):
			print "PID: "+PIDS[i].PID + " -- APP: "+PIDS[i].app+" -- PORT LOCAL: "+str(PIDS[i].local)
			PIDS[i].unchanged=0