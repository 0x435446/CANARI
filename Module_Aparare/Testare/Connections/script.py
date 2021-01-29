from pwn import *

for i in range(1000,1020):
	r=remote('92.81.21.126',i)
	r.recv()
	r.send('a')

