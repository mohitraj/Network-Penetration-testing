import subprocess as sp 
net = input("Enter the IP address: ")
list1 = ['ping', '-c', '1']
list1.append(net)


try :
	r = sp.check_output(list1, timeout=1).decode()
	print (r)
except sp.TimeoutExpired:
	print ("Not live11")
except Exception as e :
	print ("Not live ", type(e))