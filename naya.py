import socket
import time
import logging
import sys
import login_ui
import chat_layout
import wx
import group_creation
import threading
import group_layout

sock=socket.socket()
sock.connect (('localhost',12000))
#sock.connect (('192.168.43.150',12000))
c=0
b=str(sock.recv(1024))
if (len(b)>1):
	c=0
else:
	c=1

class Group (group_creation.Example):
	def __init__(self,parent,sock):
		group_creation.Example.__init__(self,parent,"Group Name")
		self.sock = sock

	def Group_Create (self,event):
		try:
			r=""
			g_name=self.group_name.GetValue().strip()
			if g_name != "":
				name="#"+g_name+":join"
				self.sock.send(name)
				g_chat=Group_Chat(None,self.sock,g_name)
				g_chat.Show()
			else:
				self.show_dialog(None,"Enter a valid group name","ALERT")
		except Exception,e:
			print e

	def show_dialog(self,parent,message,title):
		dial=wx.MessageDialog(parent,message,title,wx.OK|wx.ICON_INFORMATION)
		dial.ShowModal()
		dial.Destroy()


class Group_Chat (group_layout.Example):
	def __init__(self,parent,sock,name):
		group_layout.Example.__init__(self,parent,name)
		self.sock=sock
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def Send_msg(self,event):
		try:
			msg = (self.txt_send.GetValue())
			self.txt_send.SetValue("")
			self.txt_recieve.AppendText("me: "+ msg )
			self.sock.send(msg.strip())
		except Exception, e:
			print e

	def run(self):
		while True:
			try:
				recv = self.sock.recv(1024)
				u_name=""
				ip=""
				users=[]
				local_list=[]
				list_recieve = recv.split(">> ")
				try:
					m = x + "\n"
					self.txt_recieve.AppendText(str(m))
				except Exception,e:
					print e
			except Exception, e:
				print e
				pass

	def show_dialog(self,parent,message,title):
		dial=wx.MessageDialog(parent,message,title,wx.OK|wx.ICON_INFORMATION)
		dial.ShowModal()
		dial.Destroy()



class Chatting (chat_layout.Example):
	def __init__(self,parent,sock,name):
		chat_layout.Example.__init__(self,parent,"CHAT")
		self.sock = sock
		self.name=name
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def show_dialog(self,parent,message,title):
		dial=wx.MessageDialog(parent,message,title,wx.OK|wx.ICON_INFORMATION)
		dial.ShowModal()
		dial.Destroy()

	def Send_msg(self,event):
		try:
			msg = (self.txt_send.GetValue())
			self.txt_send.SetValue("")
			self.txt_recieve.AppendText("me: "+ msg )
			self.sock.send(msg.strip())
		except Exception, e:
			print e

	def run(self):
		while True:
			try:
				recv = self.sock.recv(1024)
				u_name=""
				ip=""
				users=[]
				local_list=[]
				list_recieve = recv.split(">> ")
				try:
					for x in list_recieve:
						print 1
						if x.find(" is online now") != -1:
							print x
							u_name=x.split(" ")[0]	
							users=u_name.split("$")
							for y in users:
								local_list=y.split("::")
								if local_list[1] != self.name:
									self.txt_online.AppendText(local_list[1]+"\n")
								else:
									pass
						else:
							m = x + "\n"
							self.txt_recieve.AppendText(str(m))
				except Exception,e:
					print e
			except Exception, e:
				print e
				pass
	
	def Group(self,event):
		try:
			group = Group (None, self.sock)
			group.Show(True)
		except Exception, e:
			print e

class Login(login_ui.MainFrame):
	def __init__ (self,parent,sock):
		login_ui.MainFrame.__init__(self,parent)
		self.sock = sock
		self.str = ""
		if str(b) != '0':
			self.user_text.SetValue(b)

	def show_dialog(self,parent,message,title):
		dial = wx.MessageDialog(parent,message,title,wx.OK|wx.ICON_INFORMATION)
		dial.ShowModal()
		dial.Destroy()

	def Senderu(self,event):
		try:
			user_name = (self.user_text.GetValue())
			u=user_name
			self.sock.send(user_name.strip())
			buf = self.sock.recv(1024)
			self.show_dialog(None,buf,'INFO')
			self.str = buf
		except Exception,e:
			print e
	
	def Senderp(self,event):
		try:
			password=(self.pass_text.GetValue())
			self.sock.send(password.strip())
			buf = self.sock.recv(1024)
			self.show_dialog(None,buf,'INFO')
			self.str=buf
		except Exception,e:
			print e

	def printing (self,event):
		print self.str
		f= (self.str=='##' or self.str[0]=='W')
		if f:
			#self.show_dialog(None,'LOGGED IN!','INFO')
			chat_lay = Chatting (None, self.sock,self.user_text.GetValue())
			chat_lay.Show(True)
		else:
			self.show_dialog(None,'Enter the fields correctly!','INFO')

app = wx.App(False)
fram = Login(None,sock)
fram.Show(True)
app.MainLoop()