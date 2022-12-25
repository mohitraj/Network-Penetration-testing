import socket
import struct
import binascii
import queue
from scapy.all import *
import threading,traceback

my_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
Q = queue.Queue()


def receiver():
	while True:
		try:
			pkt  = my_socket.recvfrom(2048)
			num = int(f'{pkt[0][14]:x}')
			#print ("num", num)
			ip_length = (int(num) % 10) * 4
			ip_last_range = 14+ip_length
			ipheader = pkt[0][14:34]
			ip_hdr = struct.unpack("!12s4s4s",ipheader)
			S_ip =socket.inet_ntoa(ip_hdr[1])
			D_ip =socket.inet_ntoa(ip_hdr[2])
			print ("ip_last_range", ip_last_range)
			tcpheader = pkt[0][ip_last_range:ip_last_range+20]
			tcp_hdr = struct.unpack("!HHL4sBB6s",tcpheader)
			S_port = tcp_hdr[0]
			D_port = tcp_hdr[1]
			SQN = tcp_hdr[2]
			flags = tcp_hdr[5]
			if S_ip.startswith("192.168.21"):
				if (D_port==445 or D_port==135):
					tuple1 = (S_ip,D_ip,S_port,D_port,SQN,flags)
					Q.put(tuple1)
		except Exception as e:
			print (traceback.print_tb(e.__traceback__))	

def sender():
	while True:
		d_ip,s_ip,d_port,s_port,SQN,flag = Q.get()
		
		if (s_port==445 or s_port==135) and (flag==2):
			SQN= SQN+1
			packet =IP(dst=d_ip,src=s_ip)/TCP(dport=d_port,sport=s_port,ack=SQN,flags="SA",window=64240, options=[('MSS',1460),("WScale",3)])
		else :
			SQN= SQN+1
			packet =IP(dst=d_ip,src=s_ip)/TCP(dport=d_port,sport=s_port,ack=SQN,seq=SQN,flags="RA",window=0)	
		send(packet) 


r = threading.Thread(target=receiver)
r.start()

s = threading.Thread(target=sender)
s.start()

