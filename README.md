# C.A.N.A.R.I.

- ##### CANARI Actually Not Another Regular IDS

#### Installation & Configuration

Install pip3 using this command:

```
sudo apt install python3-pip
```

Install flask using pip3:

```
pip3 install flask
```

Next, we have to install and configure MySQL server for our database:

```
sudo apt install mysql-server
sudo apt-get install libmysqlclient-dev
sudo apt-get install libmariadbclient-dev
```

Now we have to link the MySQL server with the Python code so we have to install the mysqlclient library:

```
pip3 install mysqlclient
sudo pip3 install mysqlclient 
```

Let's configure the database

```
mysqladmin -u root password defaultpassword
mysql -u root -p
CREATE DATABASE licenta;
mysql -u root -p licenta < licenta.sql
```

We have to check our IPs, so we have to install net-tools

```
sudo apt install net-tools
```

Next, we have to install mitmproxy to set up our MITM and for this one we need this set of commands:

```
pip3 install mitmproxy
pip3 install mitmdump
sudo pip3 install mitmdump
sudo useradd --create-home mitmproxyuser
sudo -u mitmproxyuser -H bash -c 'cd ~ && pip3 install --user mitmproxy'
```

Other used libraries:

```
sudo apt install tshark
sudo apt install binwalk
pip3 install virustotal-api-v2
pip3 install pycryptodome
```

We need these for our Machine Learning:

```
pip3 install tensorflow==2.4
pip3 install keras
pip3 install sklearn
```

Just a configuration file for VirusTotal API:

```
touch ~/.vt-config.json
nano ~/.vt-config.json
{"_comment": "  rename the key AUXILIARY_VT_PROJECT_DIR to something else (e.g, __AUXILIARY_VT_PROJECT_DIR) to make the key undefined", "__AUXILIARY_VT_PROJECTS_DIR": "G:/\u30de\u30a4\u30c9\u30e9\u30a4\u30d6/vtprojects", "api_key": "YOUR_API_KEY"}
```

