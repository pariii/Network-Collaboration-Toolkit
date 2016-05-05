import wx

class Example(wx.Frame):
  
    def __init__(self, parent, title):
    	
    	super(Example, self).__init__(parent, title=title, 
            size=(600, 450))
    	self.InitUI()
    	self.Centre()
    	self.Show()     
        
    def InitUI(self):
       	panel = wx.Panel(self)
       	hbox = wx.BoxSizer(wx.HORIZONTAL)
       	fgs = wx.FlexGridSizer(5, 2, 9, 25)

    	online = wx.StaticText(panel, label="Members")
    	r_msg = wx.StaticText(panel, label="Received Messages")
    	s_msg = wx.StaticText(panel, label="Send Messages")
    	blank1 = wx.StaticText(panel, label=" ")
    	blank2 = wx.StaticText(panel, label=" ")
    	blank3 = wx.StaticText(panel, label=" ")
    	blank4 = wx.StaticText(panel, label=" ")
    	self.btn = wx.Button(panel, -1, "Send")
    	self.btn.Bind(wx.EVT_BUTTON,self.Send_msg)
    	# self.group = wx.Button(panel, -1, "Create Group")
    	# self.group.Bind(wx.EVT_BUTTON,self.Group)

    	self.txt_online = wx.TextCtrl(panel)
    	self.txt_recieve = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
    	self.txt_send = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
    	fgs.AddMany([(online), (r_msg), (self.txt_online, 1, wx.EXPAND), (self.txt_recieve, 1, wx.EXPAND),(blank1) ,(s_msg),(blank3) ,(self.txt_send, 1, wx.EXPAND), (blank2), (self.btn)])
    	fgs.AddGrowableRow(1, 2) 
    	fgs.AddGrowableCol(1, 1)
    	hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
    	panel.SetSizer(hbox)

	def Send_msg( self, event ):
		event.Skip()

	# def Group( self, event ):
	# 	event.Skip()


if __name__ == '__main__':
	app = wx.App()
	Example(None, title='Review')
	app.MainLoop()