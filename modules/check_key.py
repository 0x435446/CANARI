from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def check(public,private):
	try:
		fd = open(public, "rb")
		public_key = fd.read()
		fd.close()
		rsa_key = RSA.importKey(public_key)
		rsa_key = PKCS1_OAEP.new(rsa_key)
		w=b"Salut"
		encrypted = rsa_key.encrypt(w)
		fd2 = open(private, "rb").read()
		private_key = RSA.importKey(fd2)
		private_key = PKCS1_OAEP.new(private_key)
		decrypted = private_key.decrypt(encrypted)
		if w == decrypted:
			return 1
	except:
		pass
	return 0