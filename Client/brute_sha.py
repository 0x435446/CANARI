import hashlib

cuvant = "cR0VmsAjgm!30x!".encode()
i = 0
ok = 1
while(ok):
	sha = hashlib.sha256((cuvant.decode()+str(i)).encode()).hexdigest()
	if sha[:3] == '000':
		print (sha)
		print (cuvant.decode()+str(i))
		ok = 0
	i += 1