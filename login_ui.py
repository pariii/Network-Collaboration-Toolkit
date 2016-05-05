# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 250,129 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.user_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.user_text, 0, wx.ALL, 5 )
		
		self.user_name_verify = wx.Button( self, wx.ID_ANY, u"verify", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gSizer2.Add( self.user_name_verify, 0, wx.ALL, 5 )
		
		self.pass_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.pass_text, 0, wx.ALL, 5 )
		
		self.password_verify = wx.Button( self, wx.ID_ANY, u"veify", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gSizer2.Add( self.password_verify, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		self.Login = wx.Button( self, wx.ID_ANY, u"Login", wx.Point( 50,20 ), wx.DefaultSize, 0 )
		bSizer3.Add( self.Login, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.user_name_verify.Bind( wx.EVT_BUTTON, self.Senderu )
		self.password_verify.Bind( wx.EVT_BUTTON, self.Senderp )
		self.Login.Bind( wx.EVT_BUTTON, self.printing )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Senderu( self, event ):
		event.Skip()
	
	# Virtual event handlers, overide them in your derived class
	def Senderp( self, event ):
		event.Skip()
	
	def printing( self, event ):
		event.Skip()
	

