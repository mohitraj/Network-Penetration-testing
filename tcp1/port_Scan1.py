import threading 
import time 
import socket, subprocess,sys 

def scantcp(ip,port,c=1):
	try :
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(c)
		result = sock.connect_ex((ip,port))
		if result==0:
			print (f"Port Open ",port,)
		sock.close()

	except KeyboardInterrupt:
		sock.close()
		sys.exit()

print ("Press Ctrl+c to close")
scantcp("192.168.21.1",135)