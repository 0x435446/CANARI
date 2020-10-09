import sys
import subprocess
sys.path.append('../')
from Utility import *
from Methods import *



times=[]

ip=get_ip_address('eth0')  
#ip='kali'
print ip

while(1):
    cmd="tcpdump -i eth0 -xx -c1 -l -v icmp[icmptype] == icmp-echo and icmp[icmptype] != icmp-echoreply"
    result = subprocess.check_output(cmd, shell=True).replace('\t','').split('\n')
    res=[]
    ok=0
    print result[1]
    if ip+" >" in result[1] :
    	for k in range(len(times)):
    		if(times[k].ip==get_stranger_ip(result[1])):
    			times[k].add(int(timp.time()))
                ok=1
        if ok==0 :
        	x=ICMP(int(timp.time()),get_stranger_ip(result[1]))
        	print "UNUL NOU"
        	times.append(x)
        time=result[0].split(' ')[0]
        del result[0] 	
        del result[0] 	
        for i in range(len(result)):
        	try:
        		res.append(result[i].split('  ')[1])
        	except:
        		pass            	
        values = ' '.join(str(v) for v in res)
        values=values.split(' ')
        times[len(times)-1].header.append(values[7:][:10])
        ICMP.check_header(times[len(times)-1])

        get_header_ip(values)
        if ckeck(values,16) ==  0:
        	if ckeck(values,97) ==  0:
        		print 'ICMP: PADDING FAILED'
