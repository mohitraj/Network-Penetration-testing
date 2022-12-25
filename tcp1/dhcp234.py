from scapy.all import *
import random
import time 
from threading import Thread 
def DHCP_discover():
	while True:
		try :
			m1  =RandMAC()._fix()
			#m1 =RandString(12,b"123456789abcdef")
			tid = random.randint(100,300)
			eth1 = Ether(src=m1,dst="ff:ff:ff:ff:ff:ff")
			print ("m11", m1)
			ip1 = IP(src='0.0.0.0',dst="255.255.255.255")
			udp1 = UDP(sport=68,dport=67)
			#bootp1 = BOOTP(chaddr=RandString(12,b"123456789abcdef"),xid=tid)
			bootp1 = BOOTP(chaddr="5d:5f:3e:3",xid=tid)
			dhcp1 = DHCP(options=[('message-type','discover'),('hostname','mohitraj'),"end"])
			dhcp_discover = eth1/ip1/udp1/bootp1/dhcp1
			print ("m1", m1)
			sendp(dhcp_discover,iface='ens33')
			time.sleep(1)


		except Exception as e :
			print (e)

DHCP_discover()