from ping3 import ping
from threading import Thread 
import time  
t1 = time.time()
net = input("Enter the IP address: ")
firstIp = net.rsplit(".",1)[0]
live_ip = []
def scan(st1, en1):
	for ip in range(st1,en1+1):
		IP = firstIp+"."+str(ip) 
		#print (IP)
		try :
			r = ping(IP, timeout=1)
			if isinstance(r,float):
				live_ip.append(IP)
		except Exception as e :
			print ("Not live ", type(e))

r1 = input("Enter the range use '-' to separate: ")

a,b = r1.split("-")
a = int(a)
b = int(b)
ip_t = 10
total_th = int((b-a)/ip_t)+1


list_thread = []
for each in range(total_th ):
	en = a+ip_t 
	print (en)
	if en > b :
		en = b 
	th = Thread(target=scan, args = (a,en))
	th.start()
	list_thread.append(th)
	a = en 

for th in list_thread:
	th.join()

print ("Live IP are ", )
print (live_ip)

t2 = time.time()
print ("Time taken", t2-t1)
