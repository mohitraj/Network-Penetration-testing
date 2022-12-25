from scapy.all import *
import struct
import sys
import pickle 
fw = open("wireless.data", "wb")
interface = 'wlx000c097012bf'

#ap_list = []
ap_list1 = []
d1 = {}
print ("Prcess ctrl+c for exit")
print ("BSSID\t\tSSID\t Channel", )
def info(fm):
	try:
		if fm.haslayer(Dot11):
			if ((fm.type == 0) & (fm.subtype==8)):
				if fm.addr2 not in ap_list1:
					ap_list1.append(fm.addr2)
					SSID = fm.info.decode()
					BSSID = fm.addr2
					channel = ord(fm[Dot11Elt:3].info)
					#channel = "A"
					print (BSSID, SSID, channel)
					list1 = [BSSID,SSID,channel]
					fw = open("wireless.data", "wb")

					d1[len(ap_list1)] = list1
					pickle.dump(d1, fw)
					fw.close()


	except KeyboardInterrupt:
		pickle.dump(ap_list, fw)
		fw.close()
		print ("File saved")
		#sys.exit()
		
	except Exception as e :
		print (e)
				
sniff(iface=interface,prn=info)
