from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
import os
import sys
import _thread

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

	db.close()
	return icmp_count,dns_count,http_count


@app.route('/')
def index():
	_thread.start_new_thread(dns.dns_start,())
	print ("DNS_STARTED")
	_thread.start_new_thread(icmp.icmp_start,())
	print ("ICMP_STARTED")
	_thread.start_new_thread(web.http_start,())
	print ("HTTP_STARTED")
	#_thread.start_new_thread(https.http_start,())
	#print ("HTTPS_STARTED")
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("SELECT * FROM alerte")
	data = list(cursor.fetchall())
	icmp_count,dns_count,http_count=select_graph()
	return render_template('index.html',data=data,len=len(data),icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%")


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
	icmp_count,dns_count,http_count=select_graph()
	return render_template('index.html',data=data,len=len(data),icmp=icmp_count,dns=dns_count,http=http_count)


if __name__ == '__main__':
	app.run(debug=True)
