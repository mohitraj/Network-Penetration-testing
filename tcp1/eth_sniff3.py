import socket 
import struct 
import binascii

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
list_flag  = ["U ","A ","P ","R ","S ","F "]
while True:
	try:
		pkt = s.recvfrom(2048)
		ethhead = pkt[0][0:14]
		eth = struct.unpack("!6s6s2s", ethhead)
		print ("Eth frame----------")
		print (binascii.hexlify(eth[1]), "-->",binascii.hexlify(eth[0]))
		num = int(f'{pkt[0][14]:x}')
		ip_length = num%10*4
		ip_last_range = 14+ip_length 
		ip_header = pkt[0][14:ip_last_range] 
		ip_hdr = struct.unpack("!12s4s4s",ip_header )
		print ("Source IP --> Destionation Ip")
		print (socket.inet_ntoa(ip_hdr[1]),"--->",socket.inet_ntoa(ip_hdr[2]) )
		print ("-----------------TCP ------------")
		tcp_header = pkt[0][ip_last_range: ip_last_range+20]
		tcp_hdr = struct.unpack("!HH9sB6s", tcp_header)
		print ("S Port ----> D Port")
		print (tcp_hdr[0],"---->", tcp_hdr[1])
		flag1 = tcp_hdr[3]
		str1 = bin(flag1)[2:].zfill(6)
		flag = ""
		i = 0 
		for each in str1:
			if each == "1":
				flag = flag+list_flag[i]
			i = i+1 
		print (flag)


	except Exception as e :
		print (e)