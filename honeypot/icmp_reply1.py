import socket
import struct
import binascii
import queue
import threading
import sys
import random
import my_logger
import traceback
Q = queue.Queue()

IP_address = 0
my_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
my_socket_s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

my_socket_s.bind(('ens33',socket.htons(0x0800)))

def calculate_checksum(source_string):
	
	countTo = (int(len(source_string) / 2)) * 2
	sum = 0
	count = 0

	# Handle bytes in pairs (decoding as short ints)
	loByte = 0
	hiByte = 0
	while count < countTo:
		if (sys.byteorder == "little"):
			loByte = source_string[count]
			hiByte = source_string[count + 1]
		else:
			loByte = source_string[count + 1]
			hiByte = source_string[count]
		sum = sum + (ord(hiByte) * 256 + ord(loByte))
		count += 2

	# Handle last byte if applicable (odd-number of bytes)
	# Endianness should be irrelevant in this case
	if countTo < len(source_string): # Check for odd length
		loByte = source_string[len(source_string) - 1]
		sum += ord(loByte)

	sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
					  # uses signed ints, but overflow is unlikely in ping)

	sum = (sum >> 16) + (sum & 0xffff)	# Add high 16 bits to low 16 bits
	sum += (sum >> 16)					# Add carry from above (if any)
	answer = ~sum & 0xffff				# Invert and truncate to 16 bits
	answer = socket.htons(answer)

	return answer

def ip_checksum(ip_header, size):
	cksum = 0
	pointer = 0
	while size > 1:
		cksum += int((ip_header[pointer] + ip_header[pointer+1]),16)
		size -= 2
		pointer += 2
	if size: #This accounts for a situation where the header is odd
		cksum += ip_header[pointer]
        
	cksum = (cksum >> 16) + (cksum & 0xffff)
	cksum += (cksum >>16)
    
	check_sum1=  (~cksum) & 0xFFFF
	check_sum1 =  "%x" % (check_sum1,)
	return check_sum1

def ipv4_creator(ipv4_header):
	try:
		global IP_address
		#print struct.unpack("!ssssssssssssssssssss",ipv4_header)
		#print struct.unpack("!20s",ipv4_header)
		field1,ip_id,field2,ttl,protocol,checksum,ip1,ip2=struct.unpack("!4s2s2sss2s4s4s", ipv4_header)
		num = str(random.randint(1000,9999))
		ip_id = codecs.decode(str(num), 'hex')
		checksum = b'\x00\x00'
		ipv4_new_header = field1+ip_id+field2+codecs.decode("40", 'hex')+protocol+ip2+ip1
		raw_tuple =  struct.unpack("!ssssssssssssssssss",ipv4_new_header) # for checksum
		header_list=  [each.encode('hex') for each in raw_tuple]
		check_sum= str(ip_checksum(header_list, len(header_list)))
		ipv4_new_header = field1+ip_id+field2+codecs.decode("40", 'hex')+protocol+check_sum.decode('hex')+ip2+ip1
		if IP_address != ip1:
			my_logger.logger.info(socket.inet_ntoa(ip1))

		IP_address = ip1
		print ("Done")
		return ipv4_new_header
	except Exception as e :
		print (traceback.print_tb(e.__traceback__))
	
		

def icmp_creator(icmp_header,icmp_data):
	try:
		dest_addr=""
		ICMP_REPLY = 0
		seq_number = 0
		identifier =0
		header_size = 8
		packet_size = 64
		type1, code, checksum, packet_id, seq_number = struct.unpack("!BBHHH", icmp_header)
	
		cal_checksum = 0
		header = struct.pack("!BBHHH", ICMP_REPLY, 0, cal_checksum, packet_id ,seq_number )
		cal_checksum = calculate_checksum(header +icmp_data)
		#import pdb; pdb.set_trace()
		#print header
		header = struct.pack("!BBHHH", ICMP_REPLY, 0, cal_checksum, packet_id, seq_number )
		packet = header + icmp_data
		#print "****************", packet
		return packet
	except Exception as e :
		print (traceback.print_tb(e.__traceback__))


def ethernet_creator(eth_header):
	eth1,eth2,field1 = struct.unpack("!6s6s2s",eth_header)
	eth_header = eth2+eth1+field1
	return eth_header


def receiver_icmp():
	while True:
		try:
			received_packet, addr = my_socket.recvfrom(1024)
			#print ("getting ")
			protocol_type = received_packet[23] 
			#print("protocol_type", protocol_type, type(protocol_type))
			icmp_type = received_packet[34]
			#protocol_type=struct.unpack("!B",protocol_type)[0]
			#icmp_type = struct.unpack("!B",icmp_type)[0]
			#print ("icmp_type", icmp_type, type(icmp_type))
			if  protocol_type==1 and  icmp_type==8:
				eth_header = received_packet[0:14]
				ipv4_header = received_packet[14:34]
				icmpHeader = received_packet[34:42]
				icmp_data =   received_packet[42:]
				data_tuple1 = (eth_header, ipv4_header, icmpHeader,icmp_data)
				Q.put(data_tuple1)


		except Exception as e :
			print (e)
			print (traceback.print_tb(e.__traceback__))
		

def sender_icmp():
	while True:
		try:
			data_tuple1 = Q.get()
			icmp_packet = icmp_creator(data_tuple1[2],data_tuple1[3])
			ipv4_packet = ipv4_creator(data_tuple1[1])
			eth_packet = ethernet_creator(data_tuple1[0])
			frame = eth_packet+ipv4_packet+icmp_packet
			my_socket_s.send(frame)
		except Exception as e :
			print (traceback.print_tb(e.__traceback__))
		

r = threading.Thread(target=receiver_icmp)
s = threading.Thread(target=sender_icmp)
r.start()
s.start()



