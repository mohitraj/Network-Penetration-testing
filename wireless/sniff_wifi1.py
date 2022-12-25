import socket 

try:
	sniff = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,3)
	sniff.bind(("wlx000c097012bf",0x0003))

except Exception as e :
	print (e)
list1 = []
try:
	while True:
		fm1 = sniff.recvfrom(6000)
		fm = fm1[0]
		radio_tap_len = fm[2]
		#print (radio_tap_len)
		#print (fm[radio_tap_len])
		if fm[radio_tap_len] == 128:
			src_addr = fm[radio_tap_len+4+6: radio_tap_len+4+6+6 ]
			if src_addr not in list1:
				list1.append(src_addr)
				bssid = ":".join("%02x" % b for b in src_addr)
				#print (bssid)
				byte_upto_ssid = radio_tap_len+4+6+6+6+2+12+1
				ssid_len = fm[byte_upto_ssid]
				s_rate_len = fm[byte_upto_ssid+1+ssid_len+1]
				channel = fm[byte_upto_ssid+1+ssid_len+1+s_rate_len+3]
				ssid = fm[byte_upto_ssid+1: byte_upto_ssid+1+ssid_len]

				print (bssid, channel, ssid.decode())
					#print (list1)

except Exception as e :
	print (e)