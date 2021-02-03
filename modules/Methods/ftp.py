import pyshark


while(1):
	capture = pyshark.LiveCapture(interface='eth0', bpf_filter='tcp port ftp or ftp-data')
	capture.sniff(timeout=2)
	for i in range(len(capture)):
		ok=1
		file=[]
		lines=str(capture[i]).split('\n')
		for j in range(len(lines)):
			if "Request" in lines[j]:
				lines[j]=lines[j].split(': ')
				print lines[j][0],lines[j][1]
			if ok==0:
				print lines[j]
			if "DATADATA" in lines[j]:
				ok=0
			if "Packet" in lines[j]:
				ok=1
