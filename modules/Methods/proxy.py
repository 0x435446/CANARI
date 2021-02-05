from mitmproxy import http
from mitmproxy.net.http import Headers
from mitmproxy import ctx
from mitmproxy.net.http.http1.assemble import assemble_request
import time
import binwalk
import re


def verify_content(content):

	match = re.findall(r'[\w\.-]+@[\w\.-]+', content.decode('latin1'))
	if len(match)>0:
		print ("Fisier cu email-uri trimis !😍  --> ", ', '.join(match))


	match = re.findall(r'(?=[-]*(?=[A-Z]*(?=[-])))(.*)(?=[-]*(?=[A-Z]*(?=[-])))', content.decode('latin1'))
	if len(match)>0:
		if ("RSA" in content.decode('latin1') ) or ("rsa" in content.decode('latin1')):
			print ("Fisier cu chei RSA trimis!😍  -- >", ', ',content.decode('latin1'))

			
	if ("Pass" in content.decode('latin1')) or ("pass" in content.decode('latin1')) or ("PASS" in content.decode('latin1')):
		print ("Fisier cu parole trimis!😍  -- >", ', ',content.decode('latin1'))

	

def check_whitelist(word):
	x=open("../whitelist.txt","r").read().strip().split('\n')
	for i in x:
		if i in word:
			return 1;
	return 0;


def request(flow: http.HTTPFlow):
	print("URL",flow.request.pretty_url)
	x=check_whitelist(flow.request.pretty_url)
	if x==0:
		if flow.request.method == "POST" or flow.request.method == "PUT":
			ctx.log.info("Sensitive pattern found")
			flow.intercept()
			f = open("buffer", "wb")
			content=flow.request.content
			verify_content(content)
			f.write(content)
			f.close()
			for module in binwalk.scan("buffer",signature=True,quiet=True,extract=False):
				pass
			ok=0
			for result in module.results:
				if "LZMA" not in result.description and "Zlib" not in result.description:
					print (result.description.split(',')[0])
					ok=1
			if ok==0:
				print (flow.request.text)
			print (flow.request.host_header)
			flow.resume()
			ctx.log.info("Trafic blocat")



def response(flow):
	print ("AM AJUNS AICI")
