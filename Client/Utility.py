

import socket
import fcntl
import struct


class METHODS:
	@staticmethod
	def check_header(self):
   	   nr=0
   	   try:
   	   	   for i in range(len(self.header)-1,len(self.header)-3,-1):
   	   	   	   lista=self.header[:]
   	   	   	   del lista[i][2]
   	   	   	   del lista[i][5]	
   	   	   	   del lista[i-1][2]
   	   	   	   del lista[i-1][5]
   	   	   	   if(lista[i]!=lista[i-1]):
   	   	   	   	    nr+=1
   	   except:
   	       pass
   	   if nr==2:
   	      print ("ALERT: IP HEADER CHANGED")


    
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])

    
def ckeck(values,x):
	component=x
	for index in range(29,len(values)):
		number=''
		for j in range(2):
			number+=str(hex(component)[2:])
			component+=1
		if number!=values[index]:
			return 0
	return 1
    

def get_stranger_ip(result):
	result=result.replace(' ','')
	result=result.split('>')
	result[1]=result[1].split(':')
	return result[1][0]


def get_header_ip(packet):
	s=0	
	check=0
	for i in range(7,17):
		if i!=12:
			s+=int(packet[i],16)
		else:
			check=int(packet[i],16)
	if int(hex(s^0xfffff)[3:],16)!=int(hex(check+2)[2:],16):
		if int(hex(s^0xfffff)[3:],16)!=int(hex(check+3)[2:],16):
			print ("ALERT: IP CHECKSUM FAILED")
			print (int(hex(s^0xfffff)[3:],16),int(hex(check+3)[2:],16))


def read_file(fisier):
  x=[]
  if fisier == 'TLD':
    filepath = './modules/TLD/IANA.txt'
  else:
    filepath = './modules/Magic_Numbers/signatures.txt'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      x.append(line.strip())
      line = fp.readline()
      cnt += 1
  return x
