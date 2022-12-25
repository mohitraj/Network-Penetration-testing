import subprocess as sp 
import time 
net = input("Enter the IP address ")


def scan(IP):
	list1 = ['ping', '-c', '1']
	list1.append(IP)

	try:
		r = sp.check_output(list1, timeout=.5).decode()
		if "ttl" in r.lower():
			print (IP,"-->Live")
	except sp.TimeoutExpired:
		pass

	except Exception as e :
		print (e)

firstip = net.rsplit(".",1)[0]

r1 = input("Enter the range, use '-' to seprate ")

a,b = r1.split("-")
a = int(a)
b = int(b)

t1 = time.time()
for each in range(a,b+1):
	ip = firstip+"."+str(each)
	scan(ip)

t2 = time.time()
print ("time taken ", t2-t1)