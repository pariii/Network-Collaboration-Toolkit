#sender() = sending messages to client
#Server- main class for threading adn having all clients
import socket
import threading
import time
import logging

host=""
port=12000
timeout=5
buf=1024
global clients
global messages
global accounts
global online
global groups

clients= set()
messages={}
accounts={}
online={}
groups={}

class Server(threading.Thread):
	
	def __init__(self,conn,addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.ip = self.addr[0]
		self.name = ''
		self.log = 0
	
	def sender(self,promt):
		self.conn.send('%s\n>>' %(promt,))

	def login(self):
		logging.info('Connected from: %s:%s' % (self.addr[0], self.addr[1]))
		clients.add((self.conn,self.addr))

		if self.ip not in accounts:
			msg += 'Enter you name:'
			self.sender (msg)
			accounts[self.ip] = {
				'name': '',
				'password' : '',
				'last_login' : time.ctime()
			}
			while 1:
				name = self.conn.recv(buf).strip()
				if name in messages:
					self.sender('Name already exists!!')
				else:
					break
			accounts[self.ip]['name'] = name
			self.name = name
			logging.info('%s logged as %s' % (self.addr[0],self.name))
			messages[name] = []
			self.sender ('Enter your password!')
			password = self.conn.recv(buf)
			accounts[self.ip]['password'] = password.strip()
			self.log = 1
			self.sender('You have logged in!')

		else:
			self.name = accounts[self.ip]['name']
			msg += '%s, please enter your password: ' %(self.name,)
			self.sender(msg)
			while 1:
				password = self.conn.recv(buf).strip()
				if password != accounts[self.ip]['password']:
					self.sender ('Incorrect password!!')
				else:
					self.sender ('Welcome back, last login time: %s' % (accounts[self.ip]['last_login'],))
					accounts[self.ip]['last_login'] = time.ctime()
					break
			#self.conn.send(self.show_mentions(self.name))



def main():
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s.bind((host, port))
	s.listen(5)
	
	while 1:
		try:
			conn, addr=s.accept()
			server = Server(conn, addr)
			server.start()
		except Exception, e:
			print e
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Quited'