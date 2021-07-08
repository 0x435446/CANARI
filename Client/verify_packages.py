import sys
import subprocess
import time
import os
sys.path.append('../')
from Utility import *
from Methods import *



last_apt='asd'
last_pip='asd'
last_pip3='asd'



while(1):
	cmd="dpkg -l | wc -l"
	result = subprocess.check_output(cmd, shell=True)
	if last_apt!='asd':
		if last_apt!=result:
			print ("NEW PACKAGE INSTALLED --->",)
			cmd2="grep ' install ' /var/log/dpkg.log| tail -1"
			result2 = subprocess.check_output(cmd2, shell=True)
			print (result2)
	last_apt=result

	cmd3="pip list 2>/dev/null | wc -l"
	result3 = subprocess.check_output(cmd3, shell=True)[:-1]
	if last_pip!='asd':
		if last_pip!=result3:
			print ("NEW PIP PACKAGE INSTALLED")
	last_pip=result3

	cmd4="pip3 list | wc -l"
	result4 = subprocess.check_output(cmd4, shell=True)[:-1]
	if last_pip3!='asd':
		if last_pip3!=result4:
			print ("NEW PIP3 PACKAGE INSTALLED")
	last_pip3=result4
