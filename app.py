from flask import Flask
from flask import render_template,jsonify
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
import https
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
	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='HTTPS'")
	data2 = (cursor2.fetchall())
	https_count=data2[0][0]
	db.close()
	return icmp_count,dns_count,http_count,vs_count,listen_count,connect_count,https_count


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
			#_thread.start_new_thread(https.start,())
			#print ("HTTPS_STARTED")


			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			if request.method == 'POST':
				descendent = 0
				Data = request.form
				print ("AICI E DATA",Data)
				conditie = list(Data)
				del conditie[-1]
				if 'descendent' in Data:
					del conditie[-1]
					descendent = 1
				print (len(conditie))
				print (conditie)
				try:
					numar_alerte = int(Data['numar_alerte'])
				except:
					numar_alerte = 10
				print (numar_alerte)
				timestart = Data['timestart']
				timestop = Data['timestop']
				if len(conditie)>2:
					for i in range(len(conditie)):
						conditie[i]=MySQLdb.escape_string(conditie[i]).decode()
						conditie[i]="'"+conditie[i]+"'"
						print (type(conditie[i]))
					if len(timestart)>0 and len(timestop)>0:
						if descendent == 1:
							cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' order by id DESC  limit 0,"+str(numar_alerte)+"")
						else:
							cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"'limit 0,"+str(numar_alerte))
					else:
						if descendent == 1:
							cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") order by id DESC limit 0,"+str(numar_alerte))
						else:
							cursor.execute("SELECT * FROM alerte where Type in ("+', '.join(conditie)+") limit 0,"+str(numar_alerte))
					datas = list(cursor.fetchall())
				else:
					if descendent == 1:
						cursor.execute("SELECT * FROM alerte ORDER BY id DESC limit 0,"+str(numar_alerte)+"")
					else:
						cursor.execute("SELECT * FROM alerte limit 0,"+str(numar_alerte))
					print ("AM AJUNS AICI!")
					datas = list(cursor.fetchall())
			else:
				cursor.execute("SELECT * FROM alerte limit 0,10")
				datas = list(cursor.fetchall())
			
			cursor.execute("SELECT * FROM alerte")
			data = list(cursor.fetchall())

			icmp_count,dns_count,http_count,vs_count,listen_count,connect_count,https_count=select_graph()
			
			numar=[]
			numar.append(str(icmp_count))
			numar.append(str(dns_count))
			numar.append(str(http_count))
			numar.append(str(vs_count))
			numar.append(str(listen_count))
			numar.append(str(connect_count))
			numar.append(str(https_count))
			numar.append(str(icmp_count+dns_count+http_count+vs_count+listen_count+connect_count+https_count))
			
			return render_template('index.html',data=datas,len=len(datas),low_risk=search_risk("LOW")[0][0],medium_risk=search_risk("MEDIUM")[0][0],high_risk=search_risk("HIGH")[0][0]	,icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),hsc=str(100*https_count/len(data)),numar=numar)
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
			icmp_count,dns_count,http_count,vs_count,listen_count,connect_count,https_count=select_graph()
			
			numar=[]
			numar.append(str(icmp_count))
			numar.append(str(dns_count))
			numar.append(str(http_count))
			numar.append(str(vs_count))
			numar.append(str(listen_count))
			numar.append(str(connect_count))
			numar.append(str(https_count))
			numar.append(str(icmp_count+dns_count+http_count+vs_count+listen_count+connect_count+https_count))
			
			return render_template('index.html',data=datas,len=len(datas),low_risk=search_risk("LOW")[0][0],medium_risk=search_risk("MEDIUM")[0][0],high_risk=search_risk("HIGH")[0][0]	,icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),hsc=str(100*https_count/len(data)),numar=numar)
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
	return redirect("/login")


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
	try:
		if session['loggedin'] == True:
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
		else:
			redirect("/login")
	except:
		redirect("/login")


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






@app.route('/process-rule',methods=['POST'])
def processRules():
	try:
		if session['loggedin'] == True:
			if request.method == 'POST':
				string = request.form['protocol']+":"+request.form['host']+":"+request.form['destination']+":"+request.form['others']+":"+request.form['offset']+":"+request.form['bytes']+":"+request.form['risk']+":"+request.form['message']
				print (string)
				if "::" not in string:
					print ("AM AJUNS AICI!")
					if string.count(':') != 7:
						pass
					else:
						f=open("./modules/Rules/rules.txt", "a+")
						f.write(string+"\n")
						f.close()
				return redirect('/previewRules')
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")



@app.route('/update_edit',methods=['POST'])
def processUpdate():
	try:
		print ("AM AJUNS AICI LA UPDATE")
		if session['loggedin'] == True:
			if request.method == 'POST':
				print ("AICI E ID",request.form['button_id'])

				id_alert = MySQLdb.escape_string(request.form['button_id']).decode()
				db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
				cursor = db.cursor()
				cursor.execute("SELECT * FROM alerte WHERE ID='"+id_alert+"'")
				data = list(cursor.fetchall())
				db.close()
				dictionar={}
				dictionar['ID']=data[0][0]
				dictionar['Type']=data[0][1]
				dictionar['Message']=data[0][2]
				dictionar['Risk']=data[0][3]
				dictionar['Source']=data[0][4]
				dictionar['Destination']=data[0][5]
				dictionar['Payload']=data[0][6]
				dictionar['Timestamp']=data[0][7]
				Text= ''
				try:
					Text="<div class = 'edit_left_text'>ID: "+str(dictionar['ID'])+"</div><br>"+ "<div class = 'edit_left_text'>Type: "+str(dictionar['Type'])+"</div><br>"+ "<div class = 'edit_left_text'>Mesaj: "+str(dictionar['Message'])+"</div><br>"+ "<div class = 'edit_left_text'>Risc: "+str(dictionar['Risk'])+"</div><br>"+ "<div class = 'edit_left_text'>Sursa: "+str(dictionar['Source'])+"</div><br>"+ "<div class = 'edit_left_text'>Destinatie: "+str(dictionar['Destination'])+"</div><br>"+ "<div class = 'edit_left_text'>Payload: "+str(dictionar['Payload'])+"</div><br>"+ "<div class = 'edit_left_text'>Timestamp: "+str(dictionar['Timestamp'])+"</div><br>"
					Text+="|"
					Text+="<button class='edit_right_buttons' onclick=post_edit_details_destination('"+str(dictionar['Destination'])+"')> Block/Unblock destination </button>"
					if dictionar['Type'] == "HTTP" or dictionar['Type'] == "HTTPS":
						if "User" in dictionar['Message']:
							Text+="<button class='edit_right_buttons'onclick=post_edit_details_payload('"+str(dictionar['Payload']).replace(' ','*')+"')> Block/Unblock Payload </button>"
				except:
					print ("Noti noti")
					pass
				print ("AM AJUNS AICI,DA")
				#return jsonify(dictionar)
				return Text

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")


def add_delete_destination(destination):
	file=open("./modules/whitelist.txt","r")
	content = file.read().strip().split()
	file.close()
	if destination in content:
		content.remove(destination)
		modify = open("./modules/whitelist.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(destination)
	modify = open("./modules/whitelist.txt","w")
	modify.write('\n'.join(content))
	modify.close()
	return 1


def add_delete_soruces(sources):
	file=open("./modules/whitelist_sources.txt","r")
	content = file.read().strip().split()
	file.close()
	if sources in content:
		content.remove(sources)
		modify = open("./modules/whitelist_sources.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(sources)
	modify = open("./modules/whitelist_sources.txt","w")
	modify.write('\n'.join(content))
	modify.close()
	return 1



@app.route('/edit_destionation',methods=['POST'])
def edit_destionation():
	try:
		if session['loggedin'] == True:
			if request.method == 'POST':
				print ("AICI E ID",request.form['button_id'])
				destinatie = MySQLdb.escape_string(request.form['button_id']).decode()
				if (destinatie!="-"):
					print ("dada")
					print ("AICI VEDEM DACA E SAU NU",add_delete_destination(destinatie))
				else:
					print ("Nunu")
				return destinatie

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")


def add_delete_payload(payload):
	payload=payload.replace('*',' ')
	print ("PAYLOAD",payload)
	file=open("./modules/whitelist_user_agent.txt","r")
	content = file.read().strip().split('\n')
	file.close()
	if payload in content:
		content.remove(payload)
		modify = open("./modules/whitelist_user_agent.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(payload)
	modify = open("./modules/whitelist_user_agent.txt","w")
	modify.write('\n'.join(content))
	modify.close()
	return 1



@app.route('/edit_payload',methods=['POST'])
def edit_payload():
	try:
		if session['loggedin'] == True:
			if request.method == 'POST':
				payload = MySQLdb.escape_string(request.form['button_id']).decode()
				if (payload!="-"):
					print ("dada")
					print ("AICI VEDEM DACA E SAU NU",add_delete_payload(payload))
				else:
					print ("Nunu")
				return payload

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")



def read_whitelist(path):
	x=open(path,'r')
	content = x.read().strip().split('\n')
	x.close()
	return content


@app.route('/preview_whitelist',methods=['GET'])
def preview_whitelist():
	try:
		if session['loggedin'] == True:
			content_whitelist = read_whitelist('./modules/whitelist.txt')
			content_whitelist_user_agent = read_whitelist('./modules/whitelist_user_agent.txt')
			content_whitelist_sources = read_whitelist('./modules/whitelist_sources.txt')
			return render_template('preview.html',content_whitelist=content_whitelist,len_whitelist=len(content_whitelist),content_whitelist_user_agent=content_whitelist_user_agent,len_content_whitelist_user_agent=len(content_whitelist_user_agent),content_whitelist_sources=content_whitelist_sources,len_content_whitelist_sources=len(content_whitelist_sources))
		else:
			return redirect("/login")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")






@app.route('/update_whitelist',methods=['POST'])
def update_whitelist():
	print ("AM AJUNS AICI BAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	try:
		if session['loggedin'] == True:
			print (request.form)
			if request.form['type'] == '1':
				add_delete_destination(request.form['data'])
			if request.form['type'] == '2':
				add_delete_payload(request.form['data'])
			if request.form['type'] == '3':
				add_delete_soruces(request.form['data'])
			return "Done!"
		else:
			return redirect("/login")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")




@app.route('/previewRules',methods=['GET'])
def preview_rules():
	try:
		if session['loggedin'] == True:
			rules = read_whitelist('./modules/Rules/rules.txt')
			update_rules=[z.replace(':',' : ') for z in rules if z[0]!='#' ]
			print (update_rules)
			return render_template('add_rules.html',rules=update_rules,len=len(update_rules))

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")




if __name__ == '__main__':
	app.run(debug=True)
