from scapy.all import * 
import pickle 

fr = open("wireless.data", "rb")
data = pickle.load(fr)
for k,v in data.items():
	print (k,v)

interface = "wlx000c097012bf"

num1 = int(input("Enter your choice "))
target = data.get(num1)[0]

list1 = []
def info(fm):
	if fm.haslayer(Dot11):
		if ((fm.type==2) ):
			if fm.addr2 == target:
				#if fm.addr1 not in list1:
					print ("connected are ", fm.addr1, "\t",fm.addr2,"\t", fm.addr3)
					#list1.append(fm.addr1 )

sniff(iface=interface,prn=info)