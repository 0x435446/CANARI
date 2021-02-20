from Crypto.PublicKey import RSA

def generate_pair(username):
	key = RSA.generate(2048)
	f = open("./modules/privateKeys/private"+username+".pem", "wb")
	f.write(key.exportKey('PEM'))
	f.close()

	pubkey = key.publickey()
	f = open("./modules/publicKeys/"+username+".pem", "wb")
	f.write(pubkey.exportKey('PEM'))
	f.close()

