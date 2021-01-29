from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
import MySQLdb 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlagFlag123.'
app.config['MYSQL_DB'] = 'BlockIT'

mysql = MySQL(app)


#FlagFlag123.


@app.route('/hello/')
def hello(name="a"):
    return render_template('hello.html', name=name)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/DNS')
def data_dns():
    db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="BlockIT" )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM dns")
    data = list(cursor.fetchall())
    for i in range(len(data)):
        data[i]=list(data[i])
        del data[i][0]
        del data[i][0]
        aux=data[i][1]
    cursor.execute("SELECT Protocol FROM events")
    menu = list(cursor.fetchall())
    db.close()
    
    return render_template('data.html',data=data,len=len(data),menu=menu,menu_len=len(menu))



@app.route('/data/HTTP')
def data_http():
    db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="BlockIT" )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM http")
    data = list(cursor.fetchall())
    for i in range(len(data)):
        data[i]=list(data[i])
        del data[i][0]
        del data[i][0]
        aux=data[i][1]
    cursor.execute("SELECT Protocol FROM events")
    menu = list(cursor.fetchall())
    db.close()
    
    return render_template('data.html',data=data,len=len(data),menu=menu,menu_len=len(menu))






@app.route('/data/ICMP')
def data_icmp():
    db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="BlockIT" )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM icmp")
    data = list(cursor.fetchall())
    for i in range(len(data)):
        data[i]=list(data[i])
        del data[i][0]
        del data[i][0]
        aux=data[i][1]
    cursor.execute("SELECT Protocol FROM events")
    menu = list(cursor.fetchall())
    db.close()
    
    return render_template('data.html',data=data,len=len(data),menu=menu,menu_len=len(menu))









if __name__ == '__main__':
    app.run(debug=True)
