#!/usr/bin/env python3

import threading
import socket

def getOptions():
	'''
	Function for showing server commands
	''' 
	return ("---OPTIONS:\n---addName deleteName getClientsList getAddress exit")

def addName(name,ipaddress,port):
	'''
	Function for adding new client to active clients list
	'''
	
	with open("clients", 'r+') as clients:
		for line in clients:
			if name in line:
				print("Trying rewrite name")
				return 0
			if ipaddress+':'+port in line:
				print("Trying rewrite socket")
				return 0
		clients.write(name+' '+ipaddress+':'+port+'\r\n')
		print("Client "+name+" is added in the list")
		return 1

def deleteName(name):
	'''
	Function for deleting client from active clients list
	'''
	with open("clients", 'r+') as clients:
		lines=clients.readlines()
		clients.seek(0)
		check=0
		for line in lines:
			if name not in line:
				clients.write(line)
			else:
				check=1
			clients.truncate()
		if check:
			print(name, ' was deleted from the list')
			return check
		else:
			print('Trying delete uncorrect name')
			return check

def getClientsList():
	'''
	Function for getting active clients list
	'''
	with open("clients") as clients:
		names=""
		for line in clients:
			names+=line.rsplit()[0]+' '
	print('Somebody are getting the clients names')
	return names

def getAddress(name):
	'''
	Function for getting client socket using clients name
	'''
	with open("clients") as clients:
		for line in clients:
			if line.rsplit()[0]==name:
				print('Sendind address')
				return line.rsplit()[1]
	
	print("Trying getting address using uncorrect name")
	return ""			

def handle_client(connect,address):
	print("Connecting with ", address)
	connect.send(bytes(1))
	while True:
		#Get command
		data=connect.recv(512)
		if data==b'deleteName':
			connect.send(bytes(1))
			#Get name
			data=connect.recv(100)
			#Delete from the list
			if deleteName(data.decode('utf-8')):
				connect.send(bytes(1))
				connect.close()
				return
			else:
				connect.send(bytes(0))
		elif data==b'addName':
			connect.send(bytes(1))
			#Get name
			data=connect.recv(100)
			connect.send(bytes(addName(data.decode('utf-8'),address[0],str(address[1]))))	
		elif data==b'getClientsList':
			connect.send(getClientsList().encode('utf-8'))
		elif data==b'getAddress':
			connect.send(bytes(1))
			#Get name
			data=connect.recv(100)
			connect.send(getAddress(data.decode('utf-8').rstrip('\r\n')).encode('utf-8'))
		elif data==b'exit':
			connect.send(bytes(1))
			connect.close()
			return
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",8787))
server.listen(5)
print("Server is reading on port 8787")
while True:
	s,a=server.accept()
	t=threading.Thread(target=handle_client,args=(s,a,))
	t.start()

server.close()
#print(getClientsList())
#print(getOptions())
#print(addName("Annnnna","123.3.3.9","1234"))
#print(getAddress("Annnnna"))
#print(deleteName("Annna"))
