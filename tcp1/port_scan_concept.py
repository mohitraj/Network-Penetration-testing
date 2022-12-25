import socket

def scan_tcp(ip,port,c=1):
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket.setdefaulttimeout(c)
		result = sock.connect_ex((ip,port))
		if result==0:
			print (f"port open {port}")
		sock.close()

	except KeyboardInterrupt:
		sock.close()
		sys.exit() 

print ("Prcess Ctrl+c to close the program")

scan_tcp("192.168.21.1",135)