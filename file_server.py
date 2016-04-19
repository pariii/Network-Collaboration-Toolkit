from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def select_path():
  	PATH = raw_input('Select the Path Press Enter for default path : ') 
  	if PATH == '':
		PATH = os.getcwd()
  	
  	print PATH
  	accept_path = raw_input('Select this path?(Y/N) : ').lower().strip(' ') 
  	
  	if accept_path == 'y' or accept_path == 'Y':
		return PATH
  	else:
		select_path()

authorizer = DummyAuthorizer()
uname=raw_input("Add user name - ")
passw=raw_input("set password - ")
flag=int(raw_input("Enter 0 for read only and 1 for read and write permission - "))
PATH = select_path()
print 'selected path : ', PATH + '\n'
print uname
print passw
if (flag==1):
	authorizer.add_user(uname,passw,PATH, perm='elradfmwM')
else:
	authorizer.add_user(uname,passw,PATH)
	
authorizer.add_anonymous(PATH)

handler=FTPHandler
handler.authorizer=authorizer

address=("192.168.43.150",8080)
server=FTPServer(address,handler)

server.max_cons = 5
server.max_cons_per_ip = 2

server.serve_forever()
