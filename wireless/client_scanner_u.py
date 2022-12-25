from scapy.all import *

interface = "wlx000c097012bf"

target = input("Enter the MAC of AP ")
list1 = []
def info(fm):
	if (fm.type==2):
		if fm.addr2 == target:
			if fm.addr1 not in list1:
				print (fm.addr1," ",fm.addr2," ", fm.addr3)
				list1.append(fm.addr1)

sniff(iface=interface, prn=info)
