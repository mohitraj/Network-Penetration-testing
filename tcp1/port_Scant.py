import socket
from threading import Thread
import time 

print ("Prcess Ctrl+c to close the program")
t1 = time.time()
def scan_tcp(sp,ep,ip,c=.5):
	
	for port in range(sp,ep):
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
ip = input("Enter the IP address ")
s1 = int(input("Enter the start port "))
e1 = int(input("Enter the last port "))


total_port = e1-s1 
total_th =int(total_port/20)+1 
list_th = []
for i in range(total_th):
	e11 = s1+ 20
	if e11 > e1 :
		e11
	th1 = Thread(target=scan_tcp, args=(s1,e11,ip))
	th1.start()
	s1 = e11 
	list_th.append(th1)

for th in list_th:
	th.join()


t2 = time.time()
print ("Time taken ", t2-t1)



#scan_tcp("192.168.21.1",135)