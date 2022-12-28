#!/usr/bin/env python3

import socket,sys

myname="Anna-Vanna"
mysocket=('localhost',49999)
serversocket=('localhost',8787)

c=socket.socket()
c.bind(mysocket)
c.connect(serversocket)
data=c.recv(4)
if data==bytes(1):
	print("Connection with server!")
	c.send(b'addName')
	c.recv(4)
	c.send(myname.encode('utf-8'))
	data==c.recv(4)
	if data==bytes(1):
		print("Your name is added in the active clients list.")
		while True:
			command=input("ENTER OPTIONS:\n1-Show active users\n2-Show user address\n3-Connect to address\n4-Wait connection\n5-Exit\n")
			if command=='Show active users' or command=='1':
				c.send(b'getClientsList')
				print("Active users: ", c.recv(1024).decode('utf-8'))
			elif command=='Show user address' or command=='2':
				c.send(b'getAddress')
				data=input("Enter user name: ")
				c.recv(4)
				c.send(data.encode('utf-8'))
				print(data, "s address is ", c.recv(100).decode('utf-8'))
			elif command=='Connect to address' or command=='3':
				c.send(b'exit')
				c.recv(4)
				c.close()
				c=socket.socket()
				c.bind(mysocket)
				friend=input("Enter address and port: ")
				c.connect((friend.rsplit()[0],int(friend.rsplit()[1])))
				print("Enter exit to end")
				c.send(myname.encode('utf-8'))
				friend=c.recv(100).decode('utf-8')
				while True:
					data=input("You: ")
					c.send(data.encode('utf-8'))
					mess=c.recv(1024)
					print(friend,': ',mess.decode('utf-8'))				
					if data=='exit' or mess==b'exit':
						c.close()
						break					
				c.close()
				c=socket.socket()
				c.bind(mysocket)
				c.connect(serversocket)			
			elif command=='Wait connection' or command=='4':
				c.send(b'exit')
				c.recv(4)
				c.close()
				c=socket.socket()
				c.bind(mysocket)
				c.listen()
				print("Enter exit to end")
				a,b=c.accept()
				friend=a.recv(1024)
				a.send(myname.encode('utf-8'))
				while True:
					mess=a.recv(1024)
					print(friend,': ',mess.decode('utf-8'))
					data=input("You: ")
					a.send(data.encode('utf-8'))
					if data=='exit' or mess==b'exit':
						a.close()
						c.close()
						break					
				c.close()
				c=socket.socket()
				c.bind(mysocket)
				c.connect(serversocket)
			elif command=='Exit' or command=='5':
				c.send(b'deleteName')
				c.recv(4)
				c.send(myname.encode('utf-8'))
				if c.recv(4)==bytes(1):
					break
					print("Your address was deleted from active clients list.")
				else:
					c.send('exit')
					recv(4)
					print("Deleting address error!")
					break
			else:
				print("The command is not been understanding. Please, try again.")		
	else:
		print("Error: this name or address is using!")
c.close()
