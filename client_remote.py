from PIL import ImageGrab
from subprocess import *
from Tkinter import *
from socket import *
from PIL import Image, ImageTk
import thread
import os
import cStringIO
PORT = 9000
LPORT = PORT + 10
liveuser = []
cflag = 0
 
sock = socket(AF_INET,SOCK_STREAM)
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) 
#socket for checking live nodes
slive = socket(AF_INET, SOCK_DGRAM)
#connecting with server
sock.connect(("192.168.43.79",PORT))
print "1"

def start(image2):
    #mouse is clicked
    def leftclick(event):
        #outputting x and y coords to console
        x = event.x
        y = event.y
        sock.send('l' + str(x) + '~' + str(y))
        #root.quit()

    def rightclick(event):
        #outputting x and y coords to console
        x = event.x
        y = event.y
        sock.send('r' + str(x) + '~' + str(y))
        #root.quit()

    #key is pressed
    def key(event):
        keypress = event.keycode
        sock.send(str(keypress))
        #root.quit()

    def image():
        root.quit()    

    try:
        #adding the image
        print "an"
        img = Image.open(cStringIO.StringIO(image2))
        print "bn"
        img = img.resize((root.winfo_screenwidth(),root.winfo_screenheight()-50),Image.ANTIALIAS)
        print "cn"
        img = ImageTk.PhotoImage(img)
        label.config(image = img)
        
        #mouseclick and keyboard event
        label.bind("<Button-1>",leftclick)
        label.bind("<Button-3>",rightclick)
        label.bind("<Key>", key) 
        label.pack()
        root.focus_set()
        label.focus_set()
        
        #updating img after every 3 sec.
        root.after(2000,image)
        root.mainloop()
        return 0
    except:
        #print 'po'
        return 0

#image display gui
root = Tk()
root.geometry("%dx%d"%(root.winfo_screenwidth(), root.winfo_screenheight()-50))
label = Label(root)
print "2"
     
while True:
    print "3"
    msg = sock.recv(256456)
    print "4"
    image1 = msg
    #img = Image.open(cStringIO.StringIO(image1))
    #img.show()
    print "5"
    if start(image1) == 0:
        sock.send("start")
    else:
        sock.send("close")
        break
print 3

sock.close()