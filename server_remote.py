from PIL import ImageGrab
from subprocess import *
from Tkinter import *
from socket import *
import win32api, win32con
import Image, ImageTk
import thread
import os

PORT = 9000
LPORT = PORT + 10
liveuser = []
cflag = 0
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", PORT))
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.listen(1)

#socket for checking live nodes
slive = socket(AF_INET, SOCK_DGRAM)
slive.bind(("", LPORT))

def main():
    global cflag
    #starting thread for accepting msg from live nodes
    #thread.start_new_thread(recieve,())
    #sending msg to all nodes connected
    #connected()
    #main code
    conn,addr = sock.accept()
    print gethostname() + ' Connected by: ',gethostbyname(addr[0])
    #print '1'
    while True:
        try:
            #taking screenshot
            ImageGrab.grab().save("images\\img1.jpg", "JPEG")
            #sending image to client
            fp = open("images\\img1.jpg","rb")
            data = fp.read()#binary form reading
            fp.close()
            conn.sendall(data)
            #print '2'
            #recieving mouse coordinates or keypressed
            rec = conn.recv(1024)
            #print rec
            while rec != "start":
                if '~' in rec:
                    lr = rec[0]
                    rec = rec[1:]
                #    print '3'
                    x,y = map(int, rec.split('~'))
                    #mouse pos. set nd single click done
                    win32api.SetCursorPos((x,y))
                    if lr == 'l':
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
                    elif lr == 'r':
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
                elif rec == 'close':
                    cflag = 1
                    break
                elif rec:
                    keypress = int(rec)
                  #  print '4'
                    #particular key pressed
                    win32api.keybd_event(keypress,0,0,0)
                rec = conn.recv(1024)
        except:
            continue
        if cflag == 1:
            break

main()
for i in liveuser:
    slive.sendto("going",(i,LPORT))
#    print '5'