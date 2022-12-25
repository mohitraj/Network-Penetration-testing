from scapy.all import * 

interface = "wlx000c097012bf"

ap_list = []
print ("Sno\tBSSID\t\t\tSSID\tChannel")
def info(fm):
	if fm.haslayer(Dot11):
		if ((fm.type==0) & (fm.subtype==8)):
			if fm.addr2 not in ap_list:
				ap_list.append(fm.addr2)
				print (len(ap_list),fm.addr2,"\t",fm.info.decode(), ord(fm[Dot11Elt:3].info))

sniff(iface=interface,prn=info)