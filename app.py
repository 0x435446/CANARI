from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
import os
import sys
import _thread
from flask import request,redirect,session
from hashlib import sha256

sys.path.append('./modules/Methods')
import dns
import web
import icmp

sys.path.append('./modules/')
import check_key
import generate_rsa


app = Flask(__name__)

app.secret_key = 'PapanasiCuBranza123456'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlagFlag123.'
app.config['MYSQL_DB'] = 'BlockIT'

app.config['UPLOAD_FOLDER']='/tmp/upload'


mysql = MySQL(app)

#FlagFlag123.


def search_risk(risk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("SELECT Count(Risk) FROM alerte WHERE Risk='"+risk+"'")
	data = (cursor.fetchall())
	db.close()
	return data


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
	try:
		if session['loggedin'] == True:
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
				del conditie[-1]
				print (len(conditie))
				try:
					numar_alerte = int(Data['numar_alerte'])
				except:
					numar_alerte = 10
				print (numar_alerte)
				if len(conditie)>2:
					timestart = Data['timestart']
					timestop = Data['timestop']
					for i in range(len(conditie)):
						conditie[i]=MySQLdb.escape_string(conditie[i]).decode()
						conditie[i]="'"+conditie[i]+"'"
						print (type(conditie[i]))
					if len(timestart)>0 and len(timestop)>0:
						cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"'limit 0,"+str(numar_alerte))
					else:
						cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") limit 0,"+str(numar_alerte))
					datas = list(cursor.fetchall())
				else:
					cursor.execute("SELECT * FROM alerte limit 0,"+str(numar_alerte))
					print ("AM AJUNS AICI!")
					datas = list(cursor.fetchall())
			else:
				cursor.execute("SELECT * FROM alerte limit 0,10")
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
			
			return render_template('index.html',data=datas,len=len(datas),low_risk=search_risk("LOW")[0][0],medium_risk=search_risk("MEDIUM")[0][0],high_risk=search_risk("HIGH")[0][0]	,icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),numar=numar)
		else:
			return redirect("/login")
	except:
		return redirect("/login")

@app.route('/stop')
def stop():
	try:
		if session['loggedin'] == True:
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
			return render_template('index.html',data=data,len=len(data) ,low_risk=search_risk("LOW")[0][0],medium_risk=search_risk("MEDIUM")[0][0],high_risk=search_risk("HIGH")[0][0]	,  icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),numar=numar)
	except:
		pass
	return redirect("/login")

@app.route('/login')
def login():
	try:
		if session['loggedin'] == True:
			return redirect("/")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return render_template('login.html')


@app.route('/logout')
def logout():
	try:
		if session['loggedin'] == True:
			session.clear()
			return redirect("/login")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return render_template('login.html')


@app.route('/register')
def register():
	try:
		print ("E sau nu?",session['loggedin'])
		if session['loggedin'] == True:
			print ("LET's register")
			return render_template('register.html')
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")


@app.route('/process-register',methods=['POST'])
def process_register():
	if request.method == 'POST':
		username = MySQLdb.escape_string(request.form['username']).decode()
		password = MySQLdb.escape_string(request.form['password']).decode()
		generate_rsa.generate_pair(username)
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
		cursor = db.cursor()
		cursor.execute("INSERT INTO users (username,password) VALUES('"+ username +"','"+ sha256(password.encode()).hexdigest() +"')")
		db.commit()
		db.close()
	return redirect("/register")


@app.route('/process-login',methods=['POST'])
def process_login():
	if request.method == 'POST':
		print (request.form)
		username = MySQLdb.escape_string(request.form['username']).decode()
		password = MySQLdb.escape_string(request.form['password']).decode()
		private_key = request.files['file']
		print(private_key.filename)
		dirName="/tmp/uploads/"
		try:
			os.makedirs(dirName)    
			print("Directory " , dirName ,  " Created ")
		except FileExistsError:
			pass  
		if(len(private_key.filename)>0):
			private_key.save('/tmp/uploads/'+private_key.filename)
		else:
			private_key.filename='Nothing'
		x = check_key.check('./modules/publicKeys/'+username+'.pem','/tmp/uploads/'+private_key.filename)
		if x == 1:
			print ("CORRECT KEY")
			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			cursor.execute("SELECT * FROM users")
			users = list(cursor.fetchall())
			db.close()
			print (users)
			for i in range(len(users)):
				if users[i][1] == username:
					print ("USERNAME CORECT")
					if (sha256(password.encode()).hexdigest()==users[i][2]):
						print ("Logare cu success")
						session['loggedin'] = True
						session['username']=username
						print (session['loggedin'])
		else:
			print ("INCORRECT")
		try:
			os.system("rm /tmp/uploads/"+private_key.filename)
		except:
			pass
	return redirect("/login")


if __name__ == '__main__':
	app.run(debug=True)
