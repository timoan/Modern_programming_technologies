#!/usr/bin/env python3

import threading
import socket

def getOptions(sock):
	sock.send(b'OPTIONS: Get clients list, Exit, Get address')
	return

def handle_client(c,a):
		print("Connecting with ", a)
		c.send(b'Hello! Please, enter your name: ')
		data=c.recv(512)
		with open("clients", 'a') as clients:
			clients.write(data.decode('utf-8').rstrip('\r\n')+' '+a[0]+':'+str(a[1])+'\r\n')
		c.send(b'Your name is added in the list! What do you want to do?')
		while True:
			getOptions(c)
			data=c.recv(512)
			if data==b'Exit':
				c.send(b'Goobbye!')
				c.close()
				print("Sessions was closed by ", a)
				break
			elif data==b'Get clients list':
				with open("clients") as clients:
					names=""
					for line in clients:
						n=line.rsplit()[0]
						names+=str(n)+' '
					c.send(bytes(names, encoding = 'utf-8'))
			elif data==b'Get address':
				find=0
				c.send(b'Enter friends name: ')
				name=c.recv(100)
				with open("clients") as clients:
					for line in clients:
						i=line.rsplit()[0]
						j=name.decode('utf-8').rstrip('\r\n')
						if i==j:
							print('Sendind address for ')
							c.send(bytes('Address: '+line.rsplit()[1],encoding='utf-8'))
							find=1
					if find==0:
						c.send(b'Your friend is not found')
	
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost",8787))
s.listen(5)
print("Server is reading on port 8787")
threads=list()
while True:
	c,a=s.accept()
	t=threading.Thread(target=handle_client,args=(c,a,))
	t.start()

					
#						c.send(bytes('Address: '+line.rsplit()[1], encoding='utf-8')
