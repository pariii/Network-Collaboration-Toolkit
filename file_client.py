import ftplib
import os
import sys

port= 8080

def filesDir(path):
	files = os.listdir(path)
	for fl in files:
		i = int(files.index(fl))+1
		print str(i)+ ')' + '{:.<50}'.format(fl) + str(os.path.getsize(path+"/"+fl))+" B" 

def select_path():
  	PATH = raw_input('Select the Path press enter for default path : ') 
  	if PATH == '':
		PATH = os.getcwd()
  	
  	print PATH
  	accept_path = raw_input('Select this path?(Y/N) : ').lower().strip(' ') 
  	
  	if accept_path == 'y' or accept_path == 'Y':
		return PATH
  	else:
		select_path()

ftp=ftplib.FTP()
#host=raw_input("Enter Host address")
host=raw_input("enter host: ")
ftp.connect(host,port)
uname=raw_input("Enter Username")
passw=raw_input("Enter_password")
ftp.login(uname,passw)
while True:
	choice=int(raw_input("Enter 1 to download 0 to upload files and 2 to exit - "))
	if(choice==2):
		sys.exit(0)

	if (choice==1):
		listing=[]
		ftp.retrlines('LIST',listing.append)
		for i in listing:
			words=i.split()
			name=words[8]
			size=words[4]
			print '{:.<50}'.format(name) + size + " B \n"

		print "\n"
		try:
			filenamed=raw_input("Enter name of file to download")
			file1=open("C:\Users\dubey\Desktop\download\\"+filenamed,"wb")
			
			ftp.retrbinary("RETR "+filenamed,file1.write,8*1024)
			print "Download Complete"
			ftp.quit()
			file1.close()

		except:
			print "Some Error Occured!"

	elif (choice==0):
		class FtpUploadTracker:
			sizeWritten = 0
			totalSize = 0
			lastShownPercent = 0

			def __init__(self, totalSize):
				self.totalSize = totalSize
				self.sizeWritten = 0

			def handle(self, block):
				
				self.sizeWritten += 1024
				percentComplete = round((self.sizeWritten / self.totalSize) * 100)

				if (self.lastShownPercent != percentComplete):
					self.lastShownPercent = percentComplete
					print(str(percentComplete) + " percent complete ")

		try:
			PATH = select_path()
			print 'selected path : ', PATH + '\n'
			filesDir(PATH)

			filenameu=raw_input("Enter name of file to upload - ")
			totalSize = os.path.getsize(PATH+"/"+filenameu)

			uploadTracker = FtpUploadTracker(int(totalSize))            
			file=open(PATH+"/"+filenameu,"rb")
			
			ftp.storbinary("STOR "+filenameu,file,1024,uploadTracker.handle)
			ftp.quit()
			file.close()

		except OSError:
			print "Wrong name!"

		except ftplib.error_perm:
			print "You don't have write priviledges"

		else:
			print "Some ERROR has occured !"

	else:
		print "wrong input"	