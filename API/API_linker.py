import sys
import os


from APIfunctions import getDNSdatas
from APIfunctions import getHTTPdatas

sys.path.append('../modules/')
from verify_encoding import verify_encoding_API as checkEncoding
from Utility import get_ip_address as getCurrentIP
from Utility import ckeck as icmpPayloadVerify
from Utility import read_file_API as readTLD_Signitures
from Utility import checkIPs as checkLocalIPs
from Utility import check_chars as checkNonASCIIChars
from Utility import check_whitelist_API as checkWhitelist
from Network import checkIP as checkLiveIPs
from Network import checkIPsThreadAPI as checkPermanentLiveIPs
from VirusTotal import search_url as searchVirusTotalURL

sys.path.append('../modules/MachineLearning')
from predict import check_model_API as checkEncodingML
from verify_enc import count_lower_probabilities as countLowerProbabilitiesChars
from verify_enc import count_litere_mari as countUppercase
from verify_enc import count_litere_mici as countLowercase
from verify_enc import count_litere_mai_mari_de_f as countNonHexChars
from verify_enc import count_cifre as countDigits
from verify_enc import count_dots as countDots
from verify_enc import count_slashes as countSlashes
from verify_enc import count_underscore as countUnderscores
from verify_enc import count_lines as countLines
from verify_enc import get_every_len as getSubdomainsLen
from verify_enc import get_entropy as getEntropy

'''
#word, probabilities,  default:../modules/Data_encoding/probabilitati.txt
print (checkEncoding("masinute",'../modules/Data_encoding/probabilitati.txt'))

#interface
print (getCurrentIP('ens38'))

#read TLD or Signatures file
readTLD_Signitures('../modules/TLD/IANA.txt')

#check if IP is found by solution
print (checkLocalIPs('192.168.150.2', "Nu este", "Este"))

#check for Non ASCII characters
print (checkNonASCIIChars('192.168.150.2'))

#check IP in whitelist
print (checkWhitelist('192.168.0.0','../modules/Filters/whitelist_sources.txt'))

	#check for live IPs
#print (checkLiveIPs('192.168.150'))

	#permanent check for live IPs
#print (checkPermanentLiveIPs('192.168.150',10,'/tmp/tempips.txt'))


#print (checkEncodingML("bWFzaW51dGU",'../modules/MachineLearning/models/model4.5.h5','../modules/MachineLearning/probabilitati_extins.txt'))

print (countLowerProbabilitiesChars('wwwceva'))

print (getDNSdatas())

print (getHTTPdatas())
'''


