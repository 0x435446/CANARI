from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
import os
import sys
import _thread
from flask import request

sys.path.append('./modules/Methods')
import dns
import web
import icmp


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlagFlag123.'
app.config['MYSQL_DB'] = 'BlockIT'

mysql = MySQL(app)

#FlagFlag123.

def select_graph():
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )

	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='ICMP'")
	data2 = (cursor2.fetchall())
	icmp_count=data2[0][0]

	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='HTTP'")
	data2 = (cursor2.fetchall())
	http_count=data2[0][0]


	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='DNS'")
	data2 = (cursor2.fetchall())
	dns_count=data2[0][0]


	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='VirusTotal'")
	data2 = (cursor2.fetchall())
	vs_count=data2[0][0]

	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='Listening'")
	data2 = (cursor2.fetchall())
	listen_count=data2[0][0]

	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='Connections'")
	data2 = (cursor2.fetchall())
	connect_count=data2[0][0]


	db.close()
	return icmp_count,dns_count,http_count,vs_count,listen_count,connect_count


@app.route('/', methods=['GET', 'POST'])
def index():
	_thread.start_new_thread(dns.dns_start,())
	print ("DNS_STARTED")
	_thread.start_new_thread(icmp.icmp_start,())
	print ("ICMP_STARTED")
	_thread.start_new_thread(web.http_start,())
	print ("HTTP_STARTED")

	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	if request.method == 'POST':
		Data = request.form
		print ("AICI E DATA",Data)
		conditie = list(Data)
		print (len(conditie))
		if len(conditie)>2:
			timestart = Data['timestart']
			timestop = Data['timestop']
			for i in range(len(conditie)):
				conditie[i]=MySQLdb.escape_string(conditie[i]).decode()
				conditie[i]="'"+conditie[i]+"'"
				print (type(conditie[i]))
			if len(timestart)>0 and len(timestop)>0:
				cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"'")
			else:
				cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+")")
			datas = list(cursor.fetchall())
		else:
			cursor.execute("SELECT * FROM alerte")
			datas = list(cursor.fetchall())
	else:
		cursor.execute("SELECT * FROM alerte")
		datas = list(cursor.fetchall())
	
	cursor.execute("SELECT * FROM alerte")
	data = list(cursor.fetchall())

	icmp_count,dns_count,http_count,vs_count,listen_count,connect_count=select_graph()
	
	numar=[]
	numar.append(str(icmp_count))
	numar.append(str(dns_count))
	numar.append(str(http_count))
	numar.append(str(vs_count))
	numar.append(str(listen_count))
	numar.append(str(connect_count))
	numar.append(str(icmp_count+dns_count+http_count+vs_count+listen_count))
	
	return render_template('index.html',data=datas,len=len(datas),icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),numar=numar)


@app.route('/stop')
def stop():
	dns.stop_dns()
	print ("DNS_STOPPED")
	icmp.stop_icmp()
	print ("ICMP_STOPPED")
	web.stop_http()
	print ("HTTP_STOPPED")
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("SELECT * FROM alerte")
	data = list(cursor.fetchall())
	db.close()
	icmp_count,dns_count,http_count,vs_count,listen_count,connect_count=select_graph()
	numar=[]
	numar.append(str(icmp_count))
	numar.append(str(dns_count))
	numar.append(str(http_count))
	numar.append(str(vs_count))
	numar.append(str(listen_count))
	numar.append(str(connect_count))
	numar.append(str(icmp_count+dns_count+http_count+vs_count+listen_count))
	return render_template('index.html',data=data,len=len(data),icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),numar=numar)


if __name__ == '__main__':
	app.run(debug=True)
