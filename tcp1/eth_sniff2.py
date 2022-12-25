import socket
import struct
import binascii
s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
while True:
	try:
		pkt  = s.sendto(2048)
		ethhead = pkt[0][0:14]
		eth = struct.unpack("!6s6s2s",ethhead)
		print ("--------Ethernet Frame--------")
		print ("Source MAC --> Destination MAC")
		print (binascii.hexlify(eth[1]),"-->",binascii.hexlify(eth[0]))

	except Exception as e :
		print (e)