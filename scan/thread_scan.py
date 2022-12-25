import subprocess as sp 
from threading import Thread 
net = input("Enter the IP address: ")

def scan(IP):
	print (IP)
	list1 = ['ping', '-c', '1']
	list1.append(IP)
	try :
		r = sp.check_output(list1, timeout=1).decode()
		print (r)
	except sp.TimeoutExpired:
		print ("Not live11")
	except Exception as e :
		print ("Not live ", type(e))

firstIp = net.rsplit(".",1)[0]

r1 = input("Enter the range use '-' to separate: ")

a,b = r1.split("-")
a = int(a)
b = int(b)

for each in range(a,b+1):
	ip = firstIp+"."+str(each)
	scan(ip)