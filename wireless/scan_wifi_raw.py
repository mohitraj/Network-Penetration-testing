import socket 
import struct
import shelve 
import os
import sys
import traceback
'''
ch = raw_input("Press 'Y' to know previous result ")
print "USE only Ctrl+c to exit "
try :
	if ch.lower() == 'y':
		s = shelve.open("wireless_data.dat")
		print "Seq", "\tBSSID\t\t", "\tChannel", "SSID"
		keys= s.keys()
		list1 = []
		for each in keys:
			list1.append(int(each))
		list1.sort()

		for key in list1:
			key = str(key)
			print key,"\t",s[key][0],"\t",s[key][1],"\t",s[key][2]
		s.close()
		raw_input("Press any key to continue ")
except Exception as e :
	print e
	raw_input("Press any key to continue ")

'''
try:
	sniff = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 3)
	sniff.bind(("wlx000c097012bf", 0x0003))

except Exception as e :
	print (e )
ap_list =[]
print ("Seq", "\tBSSID\t", "\t\tChannel", "SSID")

#s = shelve.open("wireless_data.dat","n") 
try:
	while True :
		fm1 = sniff.recvfrom(6000)
		fm= fm1[0]
		#print ("fm",fm[2])
		radio_tap_lenght = fm[2]
		#print radio_tap_lenght
		#print ("type",fm[radio_tap_lenght] )
		if fm[radio_tap_lenght] == "\x80"  or fm[radio_tap_lenght] == 128:
			source_addr = fm[radio_tap_lenght+4+6:radio_tap_lenght+4+6+6]
			#print source_addr
			if source_addr not in ap_list:
				ap_list.append(source_addr)
				byte_upto_ssid = radio_tap_lenght+4+6+6+6+2+12+1
				a = fm[byte_upto_ssid]
				list_val = []
				#print a
				bssid = ':'.join('%02x' % b for b in source_addr)
				#bssid = fm[36:42].encode('hex')
				s_rate_length = fm[byte_upto_ssid+1 +a+1]
				channel = fm[byte_upto_ssid+1 +a+1+s_rate_length+3]
				ssid = fm[byte_upto_ssid+1:byte_upto_ssid+1 +a]
				print (len(ap_list),"\t",bssid,"\t",channel,"\t",ssid.decode())
				list_val.append(bssid)
				list_val.append(channel)
				list_val.append(ssid)
				seq = str(len(ap_list))
				
				#s[seq]=list_val
except KeyboardInterrupt:
	#s.close()
	sys.exit()

except Exception as e :
	traceback.print_exc()
	print (e )
	

