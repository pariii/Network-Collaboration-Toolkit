import wx

class Example(wx.Frame):
  
    def __init__(self, parent, title):
    	
    	super(Example, self).__init__(parent, title=title, 
            size=(250, 129))
    	self.InitUI()
    	self.Centre()
    	self.Show()     
        
    def InitUI(self):
      panel = wx.Panel(self)
      hbox = wx.BoxSizer(wx.HORIZONTAL)
      fgs = wx.FlexGridSizer(2, 2, 9, 25)
      
      group = wx.StaticText(panel, label="Group Name:")
      blank1 = wx.StaticText(panel, label=" ")
      self.group_name = wx.TextCtrl(panel)
      self.btn = wx.Button(panel, -1, "OK")
      self.btn.Bind(wx.EVT_BUTTON,self.Group_Create)

      fgs.AddMany([(group) ,(self.group_name, 1, wx.EXPAND), (blank1), (self.btn)])
      hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
      panel.SetSizer(hbox)
   
    def Group_Create(self, event):
      event.Skip()


if __name__ == '__main__':
  app = wx.App()
  Example(None, title='Review')
  app.MainLoop()

