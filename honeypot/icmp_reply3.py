import socket 
import struct 
import binascii
import queue 
from threading import Thread 
from scapy.all import *
import traceback

Q = queue.Queue()

my_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
my_socket_s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

def ping_sender():
	while True:
		try:
			dst_mac,src_mac,dst_ip,src_ip,packet_id,seq_number = Q.get()
			eth1 = Ether(src=src_mac,dst=dst_mac)
			ip1 = IP(src=src_ip, dst=dst_ip)
			ICMP1 = eth1/ip1/ICMP(type=0,id=packet_id,seq=seq_number)
			sendp(ICMP1,iface="ens33")

		except Exception as e :
			print (traceback.print_tb(e.__traceback__))

def recevier_icmp():
	while True:
		try:
			received_packet,addr = my_socket.recvfrom(1024)
			protocol_type = received_packet[23]
			icmp_type = received_packet[34]
			if protocol_type==1 and icmp_type==8:
				eth_header = received_packet[0:14]
				eth = struct.unpack("!6s6s2s",eth_header)
				src = binascii.hexlify(eth[1])
				dst = binascii.hexlify(eth[0])
				src_mac = ":".join([src.decode()[i:i+2]   for i in range(0,12,2)])
				dst_mac = ":".join([dst.decode()[i:i+2]   for i in range(0,12,2)])
				ipv4_header= received_packet[14:34]
				icmpHeader = received_packet[34:42]
				ip_hdr = struct.unpack("!12s4s4s",ipv4_header)
				src_ip = socket.inet_ntoa(ip_hdr[1])
				dst_ip = socket.inet_ntoa(ip_hdr[2])
				type1, code, checksum,packet_id,seq_number = struct.unpack("!BBHHH",icmpHeader)
				Q.put((src_mac,dst_mac,src_ip,dst_ip,packet_id,seq_number))

		except Exception as e :
			print (traceback.print_tb(e.__traceback__))		

r = Thread(target=recevier_icmp)
s = Thread(target=ping_sender)

r.start()
s.start()target