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
		print ("Fisier cu email-uri trimis ! --> ", ', '.join(match))
	if "Pass" or "pass" or "PASS" in content:
		print ("Fisier cu parole trimis! -- >", ', 'content)



def request(flow: http.HTTPFlow):
	
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