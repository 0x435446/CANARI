import subprocess
import MySQLdb 
import time

def checkIP(base):
	ips=[]
	for i in range(0,254):
		output = subprocess.check_output("ping "+base+"."+str(i)+" -c1 -W 1  &2>/dev/null", shell=True)
		if "100% packet loss" not in output.decode():
			ips.append(base+"."+str(i))
	return ' '.join(ips)



def checkMostIP():
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("SELECT Source, COUNT(Source) from alerte GROUP BY Source;")
	data = (cursor.fetchall())
	db.close()
	count = []
	ip = []
	nr = 0
	for i in data:
			if i[0] != '' and i[0]!=' ':
				count.append(str(i[1]))
				ip.append(str(i[0]))
				nr+=1
	return count,ip


def checkIPsThread():
	while(True):
		time.sleep(10)
		lista = checkIP("192.168.150")
		f = open('/tmp/ips.txt','w')
		for i in lista:
			f.write(i)
		f.close()

def checkIPsThreadAPI(base, waiting_time, temp_file):
	while(True):
		time.sleep(waiting_time)
		lista = checkIP(base)
		f = open(temp_file,'w')
		for i in lista:
			f.write(i)
		f.close()
