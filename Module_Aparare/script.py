from pwn import *

for i in range(10000):
	r=remote('92.81.21.126',10000)
	print r.recv()
