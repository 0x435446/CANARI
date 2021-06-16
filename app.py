from flask import Flask
from flask import render_template,jsonify
import json
import MySQLdb 
import os
import sys
import _thread
from flask import request,redirect,session
from hashlib import sha256
import importlib.util

sys.path.append('./modules/')
import VirusTotal
import Network

sys.path.append('./modules/Methods')
import dns
import web
import https
import icmp

sys.path.append('./Static/')
import DNS_pcap_analyse
import HTTP_pcap_analyse
import ICMP_pcap_analyse


def importPlugins():
	file = open('./API/plugins.txt','r')
	content = file.read().strip().split('\n')
	file.close()
	if len(content)>0:
		for i in content:
			spec = importlib.util.spec_from_file_location(i.split(',')[0], i.split(',')[1])
			modul = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(modul)
			_thread.start_new_thread(modul.start,())

app = Flask(__name__)

app.secret_key = 'PapanasiCuBranza123456'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlagFlag123.'
app.config['MYSQL_DB'] = 'BlockIT'

app.config['UPLOAD_FOLDER']='/tmp/upload'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']


#FlagFlag123.

def load_blacklist():
	file=open("./modules/Filters/blacklist.txt","r")
	content = file.read().strip().split()
	file.close()
	for destination in content:
		os.system('sudo iptables -A OUTPUT -p all -d '+destination+' -j DROP')


def search_risk(risk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
	cursor = db.cursor()
	cursor.execute("SELECT Count(Risk) FROM alerte WHERE Risk='"+risk+"'")
	data = (cursor.fetchall())
	db.close()
	return data

def get_whitelist_details():
	fisier = "./modules/Filters/whitelist_sources.txt"
	count1=len(open(fisier,"r").read().split("\n"))
	fisier = './modules/Filters/whitelist_user_agent.txt'
	count2=len(open(fisier,"r").read().split("\n"))
	fisier = './modules/Filters/whitelist.txt'
	count3=len(open(fisier,"r").read().split("\n"))
	return count1,count2,count3

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
	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='Anomalies'")
	data2 = (cursor2.fetchall())
	ipv4_count=data2[0][0]
	cursor2= db.cursor()
	cursor2.execute("SELECT Count(Type) FROM alerte WHERE Type='Machine Learning'")
	data2 = (cursor2.fetchall())
	ml=data2[0][0]
	db.close()
	return icmp_count,dns_count,http_count,vs_count,listen_count,connect_count,https_count,ipv4_count,ml


@app.route('/load_blacklist')
def load():
	try:
		if session['loggedin'] == True:
			load_blacklist()
			return redirect("/")
	except:
		pass
	return redirect("/login")



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
			try:
				_thread.start_new_thread(Network.checkIPsThread,())
				print ("CheckNetwork_Started")
			except:
				print ("NAHHHHHH")
				pass
			
			importPlugins()

			#load_blacklist()		
			#_thread.start_new_thread(https.start,())
			#print ("HTTPS_STARTED")
			
			whitelist_c1,whitelist_c2,whitelist_c3 = get_whitelist_details()
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
					pass
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
					print ("DA")
					datas = list(cursor.fetchall())
			else:
				cursor.execute("SELECT * FROM alerte limit 0,10")
				datas = list(cursor.fetchall())
			
			cursor.execute("SELECT * FROM alerte")
			data = list(cursor.fetchall())

			icmp_count,dns_count,http_count,vs_count,listen_count,connect_count,https_count,ipv4_count,ml_count=select_graph()
			
			numar=[]
			numar.append(str(icmp_count))
			numar.append(str(dns_count))
			numar.append(str(http_count))
			numar.append(str(vs_count))
			numar.append(str(listen_count))
			numar.append(str(connect_count))
			numar.append(str(https_count))
			numar.append(str(ipv4_count))
			numar.append(str(ml_count))
			numar.append(str(icmp_count+dns_count+http_count+vs_count+listen_count+connect_count+https_count+ipv4_count+ml_count))
			
			return render_template('index.html',ml_count=str(100*ml_count/len(data)), ipv4_count=str(100*ipv4_count/len(data)),whitelist_c1=whitelist_c1,whitelist_c2=whitelist_c2,whitelist_c3=whitelist_c3,data=datas,len=len(datas),low_risk=search_risk("LOW")[0][0],medium_risk=search_risk("MEDIUM")[0][0],high_risk=search_risk("HIGH")[0][0]	,icmp=str(100*icmp_count/len(data))+"%",dns=str(100*dns_count/len(data))+"%",http=str(100*http_count/len(data))+"%",vt=str(100*vs_count/len(data))+"%",lc=str(100*listen_count/len(data)),cn=str(100*connect_count/len(data)),hsc=str(100*https_count/len(data)),numar=numar)
		else:
			return redirect("/login")
	except:
		return redirect("/login")


@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
	#try:
		if session['loggedin'] == True: 
			whitelist_c1,whitelist_c2,whitelist_c3 = get_whitelist_details()
			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			WeHaveEdit = 1
			forSelect ='Index, Type, Message, Risk, Source, Destination, Payload, Timestamp'
			if request.method == 'POST':
				descendent = 0
				WeHaveEdit = 0
				Data = request.form
				print ("AICI E DATA",Data)
				try:
					forSelect = Data['hiddenID']
				except:
					forSelect ='Index, Type, Message, Risk, Source, Destination, Payload, Timestamp'
					WeHaveEdit = 1
					pass
				forSelect = forSelect.replace("Index","ID")
				forSelect = forSelect[:-2]
				if("Actions" in forSelect):
					WeHaveEdit = 1
					forSelect = forSelect.replace(", Actions","")
				print ("AICI E FORSELECT:",forSelect)
				if forSelect == '':
					forSelect ='Index, Type, Message, Risk, Source, Destination, Payload, Timestamp'
					forSelect = forSelect.replace("Index","ID")
					WeHaveEdit = 1
				conditie = list(Data)
				destination =""
				if "dest" in Data and len(Data)>1:
					if Data['dest'] != "":
						destination = Data['dest']
				if "hiddenID" in Data:
					del conditie[-1]
					del conditie[-1]
				if conditie[0] != 'dest':
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
						pass
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
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' order by id DESC  limit 0,"+str(numar_alerte)+"")
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' and Destination = '"+destination+"' order by id DESC  limit 0,"+str(numar_alerte)+"")
							else:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"'limit 0,"+str(numar_alerte))
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' and Destination = '"+destination+"' limit 0,"+str(numar_alerte))
						else:
							if descendent == 1:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") order by id DESC limit 0,"+str(numar_alerte))
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Destination = '"+destination+"' order by id DESC limit 0,"+str(numar_alerte))
							else:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") limit 0,"+str(numar_alerte))
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Type in ("+', '.join(conditie)+") and Destination = '"+destination+"' limit 0,"+str(numar_alerte))
						datas = list(cursor.fetchall())
					else:
						if descendent == 1:
							if len(timestart)>0 and len(timestop)>0:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' order by id DESC limit 0,"+str(numar_alerte)+"")
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' and Destination = '"+destination+"' order by id DESC limit 0,"+str(numar_alerte)+"")
							else:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte ORDER BY id DESC limit 0,"+str(numar_alerte)+"")
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte WHERE Destination = '"+destination+"' ORDER BY id DESC limit 0,"+str(numar_alerte)+"")
						else:
							if len(timestart)>0 and len(timestop)>0:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte where Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"'limit 0,"+str(numar_alerte))
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte where Timestamp BETWEEN '"+timestart+" 00:00:00' AND '"+timestop+"' and Destination = '"+destination+"' limit 0,"+str(numar_alerte))
							else:
								if destination == "":
									cursor.execute("SELECT "+forSelect+" FROM alerte limit 0,"+str(numar_alerte))
								else:
									cursor.execute("SELECT "+forSelect+" FROM alerte WHERE Destination = '"+destination+"' limit 0,"+str(numar_alerte))
						print ("AM AJUNS AICI!")
						datas = list(cursor.fetchall())
			else:
				cursor.execute("SELECT * FROM alerte limit 0,10")
				datas = list(cursor.fetchall())
			try:
				if conditie[0] == 'dest':
					print (Data['dest'], "DATAAA")
					if len(Data) == 2:
						cursor.execute("SELECT * FROM alerte where Destination in ('"+Data['dest']+"') order by id DESC")
					#cursor.execute("SELECT * FROM alerte where Destination in ("+', '.join(Data['dest'].split(','))+")")
					else:
						cursor.execute("SELECT * FROM alerte where Destination in ('"+Data['dest']+"')")

					datas = list(cursor.fetchall())
			except:
				cursor.execute("SELECT * FROM alerte limit 0,10")
				datas = list(cursor.fetchall())
				pass
			cursor.execute("SELECT * FROM alerte")
			data = list(cursor.fetchall())
			ceva = []
			editButton = 0
			if WeHaveEdit == 1:
				forSelect+=", Actions"
				editButton = 1
			forSelect = forSelect.replace("ID","Index")
			ceva.append(tuple(forSelect.split(", ")))
			header = ceva

			return render_template('alerts.html',data=datas,len=len(datas),header=header ,header_len=len(header),editButton=editButton)
		else:
			print ("LOGIN 1")
			return redirect("/login")
	#except:
		#print ("LOGIN 2")
		#return redirect("/login")






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
		x = 1
		if x == 1:
			db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta" )
			cursor = db.cursor()
			cursor.execute("SELECT * FROM users")
			users = list(cursor.fetchall())
			db.close()
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
				else:
					print ("INCORRECT")
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
	file=open("./modules/Filters/whitelist.txt","r")
	content = file.read().strip().split()
	file.close()
	if destination in content:
		content.remove(destination)
		modify = open("./modules/Filters/whitelist.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(destination)
	modify = open("./modules/Filters/whitelist.txt","w")
	modify.write('\n'.join(content))
	modify.close()
	return 1

def add_delete_domain_blacklist(destination):
	file=open("./modules/Filters/blacklist.txt","r")
	content = file.read().strip().split()
	file.close()
	if destination in content:
		content.remove(destination)
		os.system('sudo iptables -D OUTPUT -p all -d '+destination+' -j DROP')
		modify = open("./modules/Filters/blacklist.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(destination)
	os.system('sudo iptables -A OUTPUT -p all -d '+destination+' -j DROP')
	modify = open("./modules/Filters/blacklist.txt","w")
	modify.write('\n'.join(content))
	modify.close()
	return 1



def add_delete_soruces(sources):
	file=open("./modules/Filters/whitelist_sources.txt","r")
	content = file.read().strip().split()
	file.close()
	if sources in content:
		content.remove(sources)
		modify = open("./modules/Filters/whitelist_sources.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(sources)
	modify = open("./modules/Filters/whitelist_sources.txt","w")
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
	file=open("./modules/Filters/whitelist_user_agent.txt","r")
	content = file.read().strip().split('\n')
	file.close()
	if payload in content:
		content.remove(payload)
		modify = open("./modules/Filters/whitelist_user_agent.txt","w")
		modify.write('\n'.join(content))
		modify.close()
		return 0
	content.append(payload)
	modify = open("./modules/Filters/whitelist_user_agent.txt","w")
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
			content_whitelist = read_whitelist('./modules/Filters/whitelist.txt')
			content_whitelist_user_agent = read_whitelist('./modules/Filters/whitelist_user_agent.txt')
			content_whitelist_sources = read_whitelist('./modules/Filters/whitelist_sources.txt')
			return render_template('preview.html',content_whitelist=content_whitelist,len_whitelist=len(content_whitelist),content_whitelist_user_agent=content_whitelist_user_agent,len_content_whitelist_user_agent=len(content_whitelist_user_agent),content_whitelist_sources=content_whitelist_sources,len_content_whitelist_sources=len(content_whitelist_sources))
		else:
			return redirect("/login")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")



def search_in_files(word,file):
	if file == "Sources":
		fisier = "./modules/Filters/whitelist_sources.txt"
	elif file == "UserAgent":
		fisier = './modules/Filters/whitelist_user_agent.txt'
	elif file == "Domains":
		fisier = './modules/Filters/whitelist.txt'
	elif file == "Blacklist":
		fisier = "./modules/Filters/blacklist.txt"
	print ("AICI E FILE",file)
	file2=open(fisier,"r")
	content = file2.read().strip().split('\n')
	file2.close()
	if word in content:
		return 1
	return 0




@app.route('/update_whitelist',methods=['POST'])
def update_whitelist():
	try:
		if session['loggedin'] == True:
			print (request.form)
			if request.form['type'] == '1':
				add_delete_destination(request.form['data'])
			if request.form['type'] == '2':
				add_delete_payload(request.form['data'])
			if request.form['type'] == '3':
				add_delete_soruces(request.form['data'])
			if request.form['type'] == '4':
				if search_in_files(request.form['data'],request.form['list']) == 1:
					print ("DA, E 1")
					if request.form['list'] == "Sources":
						return "Sursa exista!"
					if request.form['list'] == "UserAgent":
						return "User-Agent-ul exista!"
					if request.form['list'] == "Domains":
						return "Domeniul exista!"
				else:
					if request.form['list'] == "Sources":
						return "Nu s-a gasit sursa cautata"
					if request.form['list'] == "UserAgent":
						return "Nu s-a gasit User-Agent-ul cautat"
					if request.form['list'] == "Domains":
						return "Nu s-a gasit domeniul cautat"
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
			update_rules=[['Protocol','Host','Dest','Others','Offset','Bytes','Risk','Message']]
			rules = read_whitelist('./modules/Rules/rules.txt')
			#update_rules=[z.replace(':',' : ') for z in rules if z[0]!='#' ]
			for z in rules:
				if z[0]!='#':
					update_rules.append(z.split(':'))
			print (update_rules)
			return render_template('add_rules.html',rules=update_rules,len=len(update_rules))

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")




@app.route('/previewBlacklist',methods=['GET'])
def preview_blacklist():
	try:
		if session['loggedin'] == True:
			blacklist = read_whitelist('./modules/Filters/blacklist.txt')
			return render_template('preview_blacklist.html',blacklist=blacklist,len=len(blacklist))

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")



@app.route('/update_blacklist',methods=['POST'])
def update_blacklist():
	try:
		if session['loggedin'] == True:
			print (request.form)
			if request.form['type'] == '1':
				add_delete_domain_blacklist(request.form['data'])
			if request.form['type'] == '2':
				if (search_in_files(request.form['data'],"Blacklist") == 1):
					return "Domeniul se afla in blacklist"
				else:
					return "Domeniul nu se afla in blacklist"
			return "Done!"
		else:
			return redirect("/login")
	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")



@app.route('/checkAndroid',methods=['GET'])
def checkAndroid():
	_thread.start_new_thread(VirusTotal.search_sha,(request.args.get('sha'),request.remote_addr))
	return redirect("/")

@app.route('/checkHashes',methods=['GET'])
def checkHashes():
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="licenta")
	cursor= db.cursor()
	cursor.execute("SELECT JSON FROM applications WHERE IP='"+request.remote_addr+"'")
	data = (cursor.fetchall())
	try:
		return jsonify(data)
	except:
		return "None"

@app.route('/loadIPs',methods=['GET'])
def loadIP():
	if session['loggedin'] == True:
		ips = Network.checkIP("192.168.150")
		ip = Network.checkMostIP()
		return str(ips)+"\n"+' '.join(ip[0])+"\n"+' '.join(ip[1])
	else:
		return redirect("/login")


@app.route('/loadFile', methods=['POST'])
def upload_file():
	print ("DA")
	uploaded_file = request.files['file']
	filename = uploaded_file.filename
	if filename != '':
		file_ext = os.path.splitext(filename)[1]
		if file_ext not in app.config['UPLOAD_EXTENSIONS']:
			return "Extension not allowed"
	logs = uploaded_file.read().decode()
	lines = logs.split("\n")
	print (lines)
	for i in range(len(lines)):
		lines[i] = "<tr>\n<td>"+lines[i].replace("\t"," </td><td>\n")+"\n</tr>"
	lines.insert(0,"<table id='tabel_alerte'>")
	lines.append("</table>")
	print ('\n'.join(lines))
	mesaj = '\n'.join(lines)
	print ("AICI E MESAJUL")
	print (mesaj.replace("<td>\replace </td>",""))
	return mesaj.replace("<td>\replace </td>","")

ALLOWED_EXTENSIONS = {'pcap', 'pcapng'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pcapAnalysis',methods=['GET'])
def pacpanalyse():
	try:
		if session['loggedin'] == True:
			return render_template('pcaps.html')

	except:
		print ("NU ESTI LOGAT!")
		pass
	return redirect("/login")

@app.route('/pcapAnalysisUpload',methods=['POST'])
def pcapUpload():
	#try:
		if session['loggedin'] == True:
			file = request.files['file']
			print (file.filename)
			if (allowed_file(file.filename)):
				file.save(os.path.join('./Static/Temporary_Traffic/', file.filename))
				#----------------------------DNS------------------------------#
				domains, unique_domains, different_domains, pachete = DNS_pcap_analyse.checkTrafficDNS('./Static/Temporary_Traffic/'+file.filename)
				info_pachete = []
				for i in pachete:
					info_pachete.append(','.join(i.get_pachet()))
				
				payloads = {}
				for i in unique_domains:
					if i[0] =='.':
						i = i[1:]
					for j in pachete:
						salata = j.destination.replace(j.payload,'')
						if salata[0] == '.':
							salata=salata[1:]
						if i == salata:
							if i in payloads.keys():
								if j.tip == 'Machine Learning':
									payloads[i] = payloads[i] + j.payload
							else:
								if j.tip == 'Machine Learning':
									payloads[i] = j.payload

				json_object = json.dumps(payloads)
				#----------------------------HTTP------------------------------#


				http_alerts, files, file_alerts, destinatii = HTTP_pcap_analyse.checkHTTPTraffic('./Static/Temporary_Traffic/'+file.filename)

				http_alerts_return = []
				http_files_return = []
				http_file_alerts = []

				for i in http_alerts:
					print (i.get_pachet())
					try:
						http_alerts_return.append('~'.join(i.get_pachet()))
					except:
						values = ','.join(map(str, i.get_pachet()))
						http_alerts_return.append('~'.join(values))

				for i in files:
					http_files_return.append('~'.join(i.get_file()))


				for i in file_alerts:
					http_file_alerts.append('~'.join(i.get_alert()))

				#----------------------------ICMP------------------------------#

				alerteICMP, destinatiiICMP, payloadsICMP = ICMP_pcap_analyse.checkICMPTraffic('./Static/Temporary_Traffic/'+file.filename)

				json_ICMP = json.dumps(payloadsICMP)
				icmp_alerts_return =[]

				for i in alerteICMP:
					icmp_alerts_return.append('~'.join(i.getItems()))

				return str(domains)+"|"+str(different_domains)+"^"+'|'.join(info_pachete)+"^"+'|'.join(unique_domains)+"^"+json_object + "^" + '|'.join(http_alerts_return) + "^" + '|'.join(http_files_return) + "^" + '|'.join(http_file_alerts)+"^"+'|'.join(destinatii)+"^"+'|'.join(icmp_alerts_return)+"^"+'|'.join(destinatiiICMP)+"^"+json_ICMP
			else:
				return "NU" 
	#except:
		#print ("NU ESTI LOGAT!")
		#pass
	#return redirect("/login")


if __name__ == '__main__':
	app.run(debug=True,host= '0.0.0.0')
