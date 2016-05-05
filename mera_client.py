import socket
import time
import logging
import sys
import login_ui
import wx

sock=socket.socket()
sock.connect (('localhost',12000))
c=0
b=str(sock.recv(1024))
if (len(b)>1):
	c=0
else:
	c=1
class Login(login_ui.MainFrame):
	def __init__ (self,parent,sock):
		login_ui.MainFrame.__init__(self,parent)
		self.sock=sock
		self.str=""
		if str(b) != '0':
			self.user_text.SetValue(b)

	def show_dialog(self,parent,message,title):
		dial=wx.MessageDialog(parent,message,title,wx.OK|wx.ICON_INFORMATION)
		dial.ShowModal()
		dial.Destroy()

	def Senderu(self,event):
		try:
			user_name=(self.user_text.GetValue())
			self.sock.send(user_name.strip())
			buf = self.sock.recv(1024)
			self.show_dialog(None,buf,'INFO')
			self.str=buf
		except Exception:
			print 'error'
	
	def Senderp(self,event):
		try:
			password=(self.pass_text.GetValue())
			self.sock.send(password.strip())
			buf = self.sock.recv(1024)
			self.show_dialog(None,buf,'INFO')
			self.str=buf
		except Exception:
			print 'error'

	def printing (self,event):
		print self.str
		f= (self.str=='##' or self.str[0]=='W')
		if f:
			self.show_dialog(None,'LOGGED IN!','INFO')
		else:
			self.show_dialog(None,'Enter the fields correctly!','INFO')

app = wx.App(False)
fram = Login(None,sock)
fram.Show(True)
app.MainLoop()