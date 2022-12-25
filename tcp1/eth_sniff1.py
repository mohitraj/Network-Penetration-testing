import socket
import struct
import binascii
s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
str2 = ["Urgent ","Ack ","Push ","Reset ","Sync ","Fin "]
while True:
	try:
		pkt  = s.recvfrom(2048)
		ethhead = pkt[0][0:14]
		eth = struct.unpack("!6s6s2s",ethhead)
		print ("--------Ethernet Frame--------")
		print ("Source MAC --> Destination MAC")
		print (binascii.hexlify(eth[1]),"-->",binascii.hexlify(eth[0]))
		print ("----------------IP----------------")
		num = int(f'{pkt[0][14]:x}')
		ip_length = (int(num)%10)*4
		ip_last_range = 14+ip_length
		ipheader = pkt[0][14:ip_last_range]
		ip_hdr = struct.unpack("!12s4s4s",ipheader)
		print ("Source IP-->  Destination IP")
		print (socket.inet_ntoa(ip_hdr[1]),"-->", socket.inet_ntoa(ip_hdr[2]))
		tcpheader = pkt[0][ip_last_range:ip_last_range+20]
		tcp_hdr = struct.unpack("!HH9sB6s",tcpheader)
		print ("Source Port--> Destination Port")
		print (tcp_hdr[0],"-->", tcp_hdr[1])
		flag1 =tcp_hdr[3]
		print(flag1)
		str1 = bin(flag1)[2:].zfill(6)
		flag = ''
		i = 0
		for each in str1:
			if each == '1':
				flag = flag+str2[i]
			i = i+1
		print (flag)


	except Exception as e :
		print (e)