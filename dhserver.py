import socket
from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

# Create a pool of addresses
IP_ADDRESS_POOL = [ '192.168.0.10',
					'192.168.0.11',
					'192.168.0.12',
					'192.168.0.13',
					'192.168.0.14',
					'192.168.0.15']

availability = [ '1',
				 '1',
				 '1',
				 '1',
				 '1',
				 '1']

def available():
	for i,n in enumerate(IP_ADDRESS_POOL):
		if (availability[i] == '1'):
			return IP_ADDRESS_POOL[i]
	
	# IF NONE AVAILABLE
	return '-1'

def stillavailable(requestedIP):
	global availability
	for i,n in enumerate(IP_ADDRESS_POOL):
		if ((IP_ADDRESS_POOL[i] == requestedIP) and (availability[i] == '1')):
			availability[i] = '0'
			print('UPDATED AVAILBILITY')
			return True
	
	# IF NONE AVAILABLE
	return False

# Create packet
def DHCP_PKT(ipAddress, MAC, transactionID, type):
	pkt = b''
	pkt += b'\x02'								# Message type: Boot Reply
	pkt += b'\x01'								# Hardware type: Ethernet
	pkt += b'\x06'								# Length
	pkt += b'\x01'								# Hops
	pkt += transactionID						# Transaction ID (4)
	pkt += b'\x00\x00'							# Seconds elapsed
	pkt += b'\x80\x00'							# Bootp flags
	pkt += b'\x00\x00\x00\x00'					# Client IP address
	pkt += inet_aton(ipAddress)					# Your client IP address (4)
	pkt += b'\x00\x00\x00\x00'					# Next server IP address
	pkt += b'\x00\x00\x00\x00'					# Relay agent IP address giadder
	pkt += MAC									# MAC address (6)
	pkt += b'\x00' * 205						# Padding, software host name, boot file name
	pkt += b'\x63\x82\x53\x63'					# Magic Cookie
	pkt += type									# DHCP Message Type (Offer or ACK) (3)
	pkt += b'\x00\x00\x00\x00\x00\x00'			# Server identifier
	pkt += b'\x33\x04\x00\x00\x0e\x10'			# IP Address Lease Time
	pkt += b'\x01\x04\xff\xff\xff\x00'			# SubnetMask
	pkt += b'\x00' * 30							# Router, DNS, Domain Name
	pkt += b'\xff'								# End
	pkt += b'\x00' * 8							# Padding
	return pkt

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

while True:
	# Recieve a UDP message
	msg, addr = s.recvfrom(1024)

	# # Print the client's MAC Address from the DHCP header
	# print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
	# for i in range(29, 34):
	# 	print(":" + format(msg[i], 'x'), end = '')
	# print()

	# # Print client's DHCP Discover
	# print("Client's DHCP Discover is " , end = '')
	# for i,n in enumerate(msg):
	# 	print(":" + format(msg[i], 'x'), end = '')
	# print()

	# Find an available IP address
	ipAddress = available()

	while (ipAddress != '-1'):
		MAC = msg[28:34]
		transactionID = msg[4:8]
		type = b'\x35\x01\x02' # type = OFFER
		pkt = DHCP_PKT(ipAddress, MAC, transactionID, type)

		# # Print client's DHCP Discover
		# print("Server's DHCP OFFER is " , end = '')
		# for i,n in enumerate(pkt):
		# 	print(":" + format(pkt[i], 'x'), end = '')
		# print()

		# Broadcast Offer
		s.sendto(pkt, DHCP_CLIENT)

		# Recieve a UDP message (Request)
		msg, addr = s.recvfrom(1024)

		# Give the first IP address && check still available?
		if (stillavailable(msg[254:257])):
			MAC = msg[28:34]
			transactionID = msg[4:7]
			type = b'\x35\x01\x05' # type = ACK
			pkt = DHCP_PKT(ipAddress, MAC, transactionID, type)

			# Broadcast ACK
			s.sendto(pkt, DHCP_CLIENT)
			ipAddress == '-1' # exit loop else keep checking new ipAddresses
		else:
			ipAddress = available()
