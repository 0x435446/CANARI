filepath = 'get.txt'
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		line=line.strip()
		line=line.replace(' ','')
		try:
			x=int(line, 16)
			if len(str(line))>1:
				print line.lower()
		except:
			pass
		line = fp.readline()
	cnt += 1
