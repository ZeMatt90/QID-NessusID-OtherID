#!/usr/bin/env python3
# 19/03/2022 rcd
#
import random


porte =10#65536
cve= ['2022-15473', '2020-123', '2021-1283','2018-15473', '2021-19256']
#numero
#'' ->unknown
protocollo = ['' , 'ICMP', 'NDP', 'SNA', 'NBF', 'IPX', 'OSPF', 'DCCP', 'IGMP', 'SCTP', 'RSVP', 'HTTP', 'FTP', 'ARP', 'BGP', 'EIGRP']

#f = open('file.txt', 'r+')
#f.truncate(0) # need '0' when using r+

with open('data.csv', 'w') as f:
	#elimino i vecchi dati
	f.truncate(0)

	f.write("ID"+','+"Port_1"+','+"Port_2"+','+"Port_3"+','+"Port_4"+','+"Port_5"+','+"Port_6"+','+"Port_7"+','+"Port_8"+','+"Port_9"+','+"Port_10"+','+"CVE"+'\n')
	for number in range (1, 80):

		f.write(str(number)+',')
		#server sezione porte
		#for porta in range (0, 65535):
		for porta in range (0, 10):

			# con probabilita' 1 su 50 mette una protocollo altrimenti mette vuoto
			if random.randint(0, 2)<1:
				f.write(protocollo[random.randint(0, 15)]+',')
			else:
				f.write(protocollo[0]+',')

		f.write(cve[random.randint(0, 4)]+'\n')

f.close()
