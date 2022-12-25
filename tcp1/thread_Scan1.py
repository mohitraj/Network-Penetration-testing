import subprocess as sp 
import time 
from threading import Thread 
net = input("Enter the IP address ")
firstip = net.rsplit(".",1)[0]

def scan(st1,en1):
	for ip in range(st1,en1):
		IP = firstip+"."+str(ip)
		list1 = ['ping', '-c', '1']
		list1.append(IP)

		try:
			r = sp.check_output(list1, timeout=.5).decode()
			if "ttl" in r.lower():
				print (IP,"-->Live")
		except sp.TimeoutExpired:
			pass

		except Exception as e :
			#print (e)
			pass



r1 = input("Enter the range, use '-' to seprate ")
a,b = r1.split("-")
a = int(a)
b = int(b)

t1 = time.time()
ip_t = 10
total_th = int((b-a)/ip_t)+1
list_thread =[] 
for each in range(total_th):
	en = a+ip_t 
	if en > b:
		en = b 
	th = Thread(target=scan, args=(a,en))
	th.start()
	list_thread.append(th)
	a = en  
for th in list_thread:
	th.join()



t2 = time.time()
print ("time taken ", t2-t1)