from Utility import *
import time as timp
import MySQLdb 
from datetime import datetime
import time
class ICMP(METHODS):
  time=[]
  def __init__(self, time,ip):
    self.header=[]
    self.htime=[]
    self.time.append(time)
    self.htime.append(time)
    self.ip=ip

  def add(self,time):
    self.time.append(time)
    self.htime.append(time)
    self.verify()

  def verify(self):
    db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
    cursor = db.cursor()
    count=0
    if len(self.time) >2:
      print ("AICI SUNT")
      if(self.time[len(self.time)-1]-self.time[len(self.time)-3]<256):
        print ("ALERTA: ICMP FREQUENCY")
        #cursor.execute("INSERT INTO icmp (ID_event,Name,Alert_Type,IP) VALUES('1', 'ICMP', 'ICMP FREQUENCY','"+str(self.ip)+"' )")
        cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('ICMP', 'HIGH FREQUENCY','MEDIUM','"+str(self.ip)+"','-','"+str(datetime.now())+"')")
        db.commit()
        for i in range(len(self.htime)):
          if self.htime[i]>int(timp.time())-3600:
            count+=1
        if count > 20 :
          print ("ALERT: ICMP / HOUR")
          #cursor.execute("INSERT INTO icmp (ID_event,Name,Alert_Type,IP) VALUES('1', 'ICMP', 'ICMP / HOUR','"+str(self.ip)+"' )")
          cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('ICMP', 'HIGH FREQUENCY / HOUR','MEDIUM','"+str(self.ip)+"','-','"+str(datetime.now())+"')")
          db.commit()



class DNS(METHODS):
  def __init__(self, domain):
    self.sd=[]
    self.d=[]
    self.time=[]
    self.d.append(domain)

  def add(self,subdomain,time):
    self.sd.append(subdomain)
    self.time.append(time)

  def check(self,domain):
    for i in range(len(self.d)):
      if self.d[i]==domain:
        return 1
    return 0


class DNS_time():
	def __init__(self,name):
		self.number=1
		self.domain=name
		self.time=str(int(time.time()))
	def add(self):
		print ("SCADEREA:",int(time.time())-int(self.time))
		if int(time.time())-int(self.time) > 3600:
			print ("COCOSEL",self.number)
			if self.number > 400:
				print ("COMMITED")
				db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
				cursor = db.cursor()
				cursor.execute("INSERT INTO alerte (Type,Message,Risk,Destination,Payload,Timestamp) VALUES('DNS', 'HIGH FREQUENCY / HOUR','HIGH','"+self.domain+"','-','"+str(datetime.now())+"')")
				db.commit()
				self.time = str(int(time.time()))
				self.number = 0
			else:
				self.number+=1
		else:
			self.number+=1




class CONNECTIONS(METHODS):
  def __init__(self):
    self.ports=[]
    self.PID=''
    self.time=[]
    self.unchanged=0
    self.alerte=0

  def add(self,port,PID,time):
    self.ports.append(port)
    self.PID=PID
    self.time.append(time)
    self.unchanged=1


class SOCKETS(METHODS):
  def __init__(self):
    self.local=[]
    self.remote=''
    self.app=''
    self.PID=''
    self.time=[]
    self.unchanged=0
    self.alerte=0

  def add(self,local,remote,PID,app,time):
    self.local.append(local)
    self.remote=remote
    self.PID=PID
    self.app=app
    self.time.append(time)
    self.unchanged=1



class WEB(METHODS):
  def __init__(self):
    self.URL=''
    self.Cookies=[]
    self.GET=[]
    self.GET_time=[]
    self.adds=0
  def add(self,URL,Cookies,GETs,GET_time):
    self.URL=URL
    self.GET.append(GETs)
    self.GET_time.append(GET_time)
    self.Cookies.append(Cookies)
    self.adds+=1
